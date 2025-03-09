from flask import Flask, request, jsonify
import instaloader
import os

app = Flask(__name__)

# Initialize Instaloader
L = instaloader.Instaloader()

@app.route("/get_post_info", methods=["GET"])
def get_post_info():
    try:
        shortcode = request.args.get("shortcode")
        if not shortcode:
            return jsonify({"error": "Shortcode parameter is required"}), 400
            
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        profile = instaloader.Profile.from_username(L.context, post.owner_username)
        
        data = {
            "Username": profile.username,
            "Full Name": profile.full_name,
            "Followers": profile.followers,
            "Following": profile.followees,
            "Post Count": profile.mediacount,
            "Engagement Rate": profile.followers / profile.mediacount if profile.mediacount > 0 else 0,
            "Is Private": profile.is_private,
            "Is Verified": profile.is_verified,
        }
        
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Get port from environment variable or default to 8080
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)