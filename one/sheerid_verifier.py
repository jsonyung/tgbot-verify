"""SheerID Student Verification Main Program — Fully updated for Advanced Anti-Detect & Command-Line Use"""
import re
import random
import logging
import time
import sys
from typing import Dict, Optional, Tuple

from . import config
from .name_generator import NameGenerator, generate_birth_date
from .img_generator import generate_images, generate_psu_email
# This file is now fully compatible with the new, advanced anti_detect.py
from .anti_detect import (
    get_sheerid_headers,
    generate_fingerprint,
    create_session,
    warm_session,
    human_delay,
)

# Configure logging in English
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


class SheerIDVerifier:
    """SheerID Student Verifier (using advanced anti-detect session)"""

    def __init__(self, verification_id: str, proxy: str = None):
        self.verification_id = verification_id
        self.device_fingerprint = generate_fingerprint()
        
        # CORRECT: It now correctly receives the 'browser_profile' from the new create_session function
        self.http_client, self.lib_name, self.browser_profile = create_session(proxy )
        
        logger.info(f"HTTP library: {self.lib_name}")
        # CORRECT: It passes the profile to the warmup function
        warm_session(self.http_client, self.browser_profile, config.PROGRAM_ID )

    def __del__(self):
        if hasattr(self, "http_client" ) and hasattr(self.http_client, "close" ):
            self.http_client.close( )

    @staticmethod
    def parse_verification_id(url: str) -> Optional[str]:
        match = re.search(r"verificationId=([a-f0-9]+)", url, re.IGNORECASE)
        return match.group(1) if match else None

    def _sheerid_request(
        self, method: str, url: str, body: Optional[Dict] = None
    ) -> Tuple[Dict, int]:
        # CORRECT: It now passes the unique browser_profile to get perfectly matching headers
        headers = get_sheerid_headers(self.browser_profile)
        human_delay(400, 900) # Small random delay between all API calls
        try:
            response = self.http_client.request(method=method, url=url, json=body, headers=headers, timeout=30 )
            try:
                data = response.json()
            except Exception:
                data = {"raw_text": response.text} if hasattr(response, 'text') else {"error": "No response text"}
            return data, response.status_code
        except Exception as e:
            logger.error(f"SheerID request failed: {e}")
            raise

    def _upload_to_s3(self, upload_url: str, img_data: bytes) -> bool:
        time.sleep(random.uniform(2, 4)) # Human-like delay before uploading a file
        try:
            resp = self.http_client.put(upload_url, content=img_data, headers={"Content-Type": "image/png"}, timeout=60 )
            if 200 <= resp.status_code < 300:
                return True
            logger.warning(f"S3 upload returned HTTP {resp.status_code}")
            return False
        except Exception as e:
            logger.error(f"S3 upload failed: {e}")
            return False

    def verify(self) -> Dict:
        try:
            name = NameGenerator.generate()
            first_name = name["first_name"]
            last_name = name["last_name"]
            school_id = config.get_random_school_id()
            school = config.SCHOOLS[school_id]
            email = generate_psu_email(first_name, last_name)
            birth_date = generate_birth_date()

            logger.info(f"Student Info: {first_name} {last_name}")
            logger.info(f"Email: {email}, School: {school['name']}, DoB: {birth_date}")
            logger.info(f"Verification ID: {self.verification_id}")

            logger.info("Step 1/4: Generating student documents...")
            assets = generate_images(first_name, last_name, school_id)
            logger.info(f"  ✅ Generated {len(assets)} documents.")

            # Main "Human Behavior" delay to defeat fraud detection
            human_like_delay = random.uniform(5, 10)
            logger.info(f"🤖 Acting human... waiting for {human_like_delay:.1f} seconds before submitting form.")
            time.sleep(human_like_delay)

            logger.info("Step 2/4: Submitting student information...")
            step2_body = {
                "firstName": first_name, "lastName": last_name, "birthDate": birth_date, "email": email,
                "organization": {"id": int(school_id), "idExtended": school["idExtended"], "name": school["name"]},
                "deviceFingerprintHash": self.device_fingerprint, "locale": "en-US",
                "metadata": {"verificationId": self.verification_id},
            }
            step2_data, step2_status = self._sheerid_request("POST", f"{config.SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/collectStudentPersonalInfo", step2_body)
            if step2_status != 200:
                raise Exception(f"Step 2 failed (Status {step2_status}): {step2_data}")
            if step2_data.get("currentStep") == "error":
                raise Exception(f"Step 2 error: {step2_data.get('errorIds', ['Unknown error'])}")

            current_step = step2_data.get("currentStep", "unknown")
            logger.info(f"✅ Step 2 complete. Current step: {current_step}")

            if current_step in ["sso", "collectStudentPersonalInfo"]:
                logger.info("Step 3/4: Skipping SSO verification...")
                step3_data, _ = self._sheerid_request("DELETE", f"{config.SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/sso")
                current_step = step3_data.get("currentStep", current_step)
                logger.info(f"✅ Step 3 complete. Current step: {current_step}")

            logger.info("Step 4/4: Requesting upload links & uploading documents...")
            files_payload = [{"fileName": asset["file_name"], "mimeType": "image/png", "fileSize": len(asset["data"])} for asset in assets]
            step4_body = {"files": files_payload}
            step4_data, _ = self._sheerid_request("POST", f"{config.SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/docUpload", step4_body)
            if not step4_data.get("documents"):
                raise Exception("Failed to get upload URLs")

            for i, doc in enumerate(step4_data["documents"]):
                logger.info(f"  📤 Uploading document {i+1}/{len(assets)}...")
                if not self._upload_to_s3(doc["uploadUrl"], assets[i]["data"]):
                    raise Exception(f"S3 upload failed for document {i+1}")
                logger.info(f"  ✅ Document {i+1} uploaded.")

            time.sleep(random.uniform(1, 3)) # Final "review" delay
            step6_data, _ = self._sheerid_request("POST", f"{config.SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/completeDocUpload")
            logger.info(f"✅ Document submission complete. Final status: {step6_data.get('currentStep')}")

            return {
                "success": True, "pending": True, "message": "Documents submitted, awaiting review.",
                "verification_id": self.verification_id, "redirect_url": step6_data.get("redirectUrl"),
            }
        except Exception as e:
            logger.error(f"❌ Verification failed: {e}")
            return {"success": False, "message": str(e), "verification_id": self.verification_id}

def main():
    """Main function for command-line execution."""
    print("=" * 60)
    print("SheerID Student Verification Tool (Command-Line Version)")
    print("=" * 60)
    print()

    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("Please enter the full SheerID verification URL: ").strip()

    if not url:
        print("❌ Error: No URL provided.")
        sys.exit(1)

    verification_id = SheerIDVerifier.parse_verification_id(url)
    if not verification_id:
        print("❌ Error: Could not find a valid 'verificationId' in the URL.")
        sys.exit(1)

    print(f"✅ Parsed Verification ID: {verification_id}")
    print()

    try:
        verifier = SheerIDVerifier(verification_id)
        result = verifier.verify()
    except Exception as e:
        logger.error(f"A critical error occurred during verification: {e}")
        result = {"success": False, "message": str(e)}

    print()
    print("=" * 60)
    print("Verification Result:")
    print("=" * 60)
    status = "✅ Success (Pending Review)" if result.get("success") else "❌ Failed"
    print(f"Status: {status}")
    print(f"Message: {result.get('message', 'No message.')}")
    if result.get("redirect_url"):
        print(f"Redirect URL: {result['redirect_url']}")
    print("=" * 60)

    return 0 if result.get("success") else 1

if __name__ == "__main__":
    exit(main())
