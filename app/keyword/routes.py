from flask import Blueprint, request, jsonify
from app.keyword.services import get_keyword_suggestions
from app.limiter import limiter
import time
from app.firestore_rate_limit import check_and_increment_usage
from app.auth_utils import get_firebase_uid_from_request

keyword_bp = Blueprint('keyword', __name__, url_prefix='/api/keywords')

@keyword_bp.route('/suggest', methods=['GET'])
@limiter.limit("10 per minute")
def suggest_keywords():
    uid, err_resp, err_code = get_firebase_uid_from_request()
    if err_resp:
        return err_resp, err_code
    if not check_and_increment_usage(uid, 'keyword_finder'):
        return jsonify({'error': 'please wait a minute before trying again'}), 429
    time.sleep(3)
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'Missing query parameter'}), 400
    suggestions = get_keyword_suggestions(query)
    return jsonify({'suggestions': suggestions})
