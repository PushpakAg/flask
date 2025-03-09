from flask import Flask, request, jsonify
import instaloader
import os

app = Flask(__name__)

L = instaloader.Instaloader()

@app.route("/get_post_info", methods=["GET"])
def get_post_info():
    try:
        shortcode = request.args.get("shortcode")
        if not shortcode:
            return jsonify({"error": "Shortcode parameter is required"}), 400

        post = instaloader.Post.from_shortcode(L.context, shortcode)

        profile = post.owner_profile  # Direct way to get profile info

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
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
