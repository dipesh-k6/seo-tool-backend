from flask import Blueprint, request, jsonify
from .services import analyze_seo
from app.limiter import limiter
import time
from app.firestore_rate_limit import check_and_increment_usage
from app.auth_utils import get_firebase_uid_from_request

seo_analyzer_bp = Blueprint('seo_analyzer', __name__)

@seo_analyzer_bp.route('/api/analyze_seo', methods=['POST'])
@limiter.limit("10 per minute")
def analyze_seo_route():
    uid, err_resp, err_code = get_firebase_uid_from_request()
    if err_resp:
        return err_resp, err_code
    if not check_and_increment_usage(uid, 'seo_analyzer'):
        return jsonify({'error': 'please wait a minute before trying again'}), 429

    time.sleep(3)
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({'error': 'URL is required.'}), 400

    try:
        result = analyze_seo(url)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
