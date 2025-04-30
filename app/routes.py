from flask import Flask, request, jsonify
from app.keyword.routes import keyword_bp
from app.seo_analyzer.routes import seo_analyzer_bp
from app.blog_title.routes import blog_title_bp
from app.limiter import limiter
from app.rank_result.routes import rank_result_bp
from flask_cors import CORS

def register_routes(app: Flask):
    CORS(app, origins=[
        "https://rankup-blogs.web.app",  #actual Firebase Hosting domain
        "http://localhost:5000",
        "http://localhost:3000",
        "http://127.0.0.1:5000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5500"
    ], allow_headers=["Content-Type", "Authorization"], methods=["GET", "POST", "OPTIONS"])
    limiter.init_app(app)
    app.register_blueprint(keyword_bp)
    app.register_blueprint(seo_analyzer_bp)
    app.register_blueprint(blog_title_bp)
    app.register_blueprint(rank_result_bp)
    app.limiter = limiter  # Attach limiter to app for use in blueprints

    @app.errorhandler(429)
    def ratelimit_handler(e):
        return jsonify({"error": "please wait a minute before trying again"}), 429