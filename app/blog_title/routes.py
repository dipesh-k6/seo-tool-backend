from flask import Blueprint, request, jsonify
from .services import get_blog_titles
from app.limiter import limiter
import time
from app.firestore_rate_limit import check_and_increment_usage
from app.auth_utils import get_firebase_uid_from_request

blog_title_bp = Blueprint('blog_title', __name__)

@blog_title_bp.route('/api/blogtitle/generate', methods=['GET'])
@limiter.limit("10 per minute")
def generate_blog_titles():
    uid, err_resp, err_code = get_firebase_uid_from_request()
    if err_resp:
        return err_resp, err_code
    if not check_and_increment_usage(uid, 'blog_title_generator'):
        return jsonify({'error': 'please wait a minute before trying again'}), 429

    time.sleep(3)
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    titles = get_blog_titles(query)
    return jsonify({"titles": titles})
