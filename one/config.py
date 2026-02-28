# SheerID 验证配置文件
import random

# SheerID API 配置
# NOTE: This Program ID is likely expired. You MUST find a new one for this to work.
PROGRAM_ID = '67c8c14f5f17a83b745e3f82' # <-- YEH ID EXPIRED HO SAKTA HAI, NAYA DHOONDNA PAD SAKTA HAI

SHEERID_BASE_URL = 'https://services.sheerid.com'
MY_SHEERID_URL = 'https://my.sheerid.com'

# 文件大小限制
MAX_FILE_SIZE = 1 * 1024 * 1024  # 1MB

# ============ University & College List (Weighted & Optimized ) ============
# weight = Higher number means it gets chosen more often.
# Focused on institutions with higher reported success rates.
SCHOOLS = {
    # ========== High Success Rate Institutions (Highest Weight) ==========
    '2565': {
        'id': 2565, 'idExtended': '2565',
        'name': 'Pennsylvania State University-Main Campus',
        'city': 'University Park', 'state': 'PA', 'country': 'US',
        'type': 'UNIVERSITY', 'domain': 'psu.edu',
        'weight': 100,
    },
    '3568': {
        'id': 3568, 'idExtended': '3568',
        'name': 'University of Michigan',
        'city': 'Ann Arbor', 'state': 'MI', 'country': 'US',
        'type': 'UNIVERSITY', 'domain': 'umich.edu',
        'weight': 98,
    },
    '378': {
        'id': 378, 'idExtended': '378',
        'name': 'Arizona State University',
        'city': 'Tempe', 'state': 'AZ', 'country': 'US',
        'type': 'UNIVERSITY', 'domain': 'asu.edu',
        'weight': 95,
    },
    '2874': {
        'id': 2874, 'idExtended': '2874',
        'name': 'Santa Monica College',
        'city': 'Santa Monica', 'state': 'CA', 'country': 'US',
        'type': 'COMMUNITY_COLLEGE', 'domain': 'smc.edu',
        'weight': 92,
    },
    '2350': {
        'id': 2350, 'idExtended': '2350',
        'name': 'Northern Virginia Community College',
        'city': 'Annandale', 'state': 'VA', 'country': 'US',
        'type': 'COMMUNITY_COLLEGE', 'domain': 'nvcc.edu',
        'weight': 90,
    },

    # ========== Top US Universities (Lower Weight) ==========
    '3499': {
        'id': 3499, 'idExtended': '3499',
        'name': 'University of California, Los Angeles',
        'city': 'Los Angeles', 'state': 'CA', 'country': 'US',
        'type': 'UNIVERSITY', 'domain': 'ucla.edu',
        'weight': 85,
    },
    '2285': {
        'id': 2285, 'idExtended': '2285',
        'name': 'New York University',
        'city': 'New York', 'state': 'NY', 'country': 'US',
        'type': 'UNIVERSITY', 'domain': 'nyu.edu',
        'weight': 85,
    },
    '1953': {
        'id': 1953, 'idExtended': '1953',
        'name': 'Massachusetts Institute of Technology',
        'city': 'Cambridge', 'state': 'MA', 'country': 'US',
        'type': 'UNIVERSITY', 'domain': 'mit.edu',
        'weight': 80,
    },
    '3113': {
        'id': 3113, 'idExtended': '3113',
        'name': 'Stanford University',
        'city': 'Stanford', 'state': 'CA', 'country': 'US',
        'type': 'UNIVERSITY', 'domain': 'stanford.edu',
        'weight': 80,
    },
}

# 默认学校
DEFAULT_SCHOOL_ID = '2565'

# UTM 参数（营销追踪参数）
DEFAULT_UTM_PARAMS = {
    'utm_source': 'gemini',
    'utm_medium': 'paid_media',
    'utm_campaign': 'students_pmax_bts-slap'
}


def get_random_school_id():
    """Weighted random selection — higher weight = more likely to be chosen."""
    ids = list(SCHOOLS.keys())
    weights = [SCHOOLS[sid].get('weight', 50) for sid in ids]
    return random.choices(ids, weights=weights, k=1)[0]
