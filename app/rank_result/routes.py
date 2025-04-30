from flask import Blueprint, request, jsonify
from app.rank_result.services import get_rank_result
from app.limiter import limiter
import time
from app.firestore_rate_limit import check_and_increment_usage
from app.auth_utils import get_firebase_uid_from_request

rank_result_bp = Blueprint('rank_result', __name__)

@rank_result_bp.route('/api/rank/track', methods=['GET'])
@limiter.limit("10 per minute")
def track_rank():
    uid, err_resp, err_code = get_firebase_uid_from_request()
    if err_resp:
        return err_resp, err_code
    if not check_and_increment_usage(uid, 'rank_tracker'):
        return jsonify({'error': 'please wait a minute before trying again'}), 429
    time.sleep(3)
    website_url = request.args.get('website_url')
    keyword = request.args.get('keyword')
    if not website_url or not keyword:
        return jsonify({"error": "Website URL and keyword are required."}), 400
    result = get_rank_result(website_url, keyword, "bing")
    return jsonify(result)
