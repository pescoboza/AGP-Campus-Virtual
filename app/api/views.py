from flask import render_template

from . import api

@api.route("/flashed-messages", methods=["POST"])
def flashed_messages():
    # TODO: remove this test
    return render_template("_flash.html")
