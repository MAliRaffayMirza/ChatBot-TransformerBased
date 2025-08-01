from sentence_transformers import SentenceTransformer, util
import os
from flask import Flask, request, redirect
import torch
import warnings
app=Flask("__name__")
warnings.filterwarnings("ignore", category=FutureWarning)

model = SentenceTransformer('all-MiniLM-L6-v2')

with open("data.txt", "r", encoding="utf-8") as file:
  knowledgebase=file.readlines()

with open("questions.txt", "r", encoding="utf-8") as file:
  questionbase=file.readlines()

questionbase_embed = model.encode(questionbase, convert_to_tensor=True)

@app.route("/")
def AIhtml():
	with open("data.txt", "r", encoding="utf-8") as file:
		knowledgebase=file.readlines()

	knowledgebase_embed = model.encode(knowledgebase, convert_to_tensor=True)
	with open("iframe.txt") as file:
		htmlm=file.read()
	return"""


<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Ali Chat</title>
</head>
<body style="margin: 0; padding: 0; height: 100vh; font-family: 'Segoe UI', sans-serif; background-color: white; color: black;">

  <div style="width: 75%; height: 100vh; position: relative; margin: 0 auto; padding: 0; box-sizing: border-box; display: flex; flex-direction: column;">

    <div id="chatbox" style="
      width: 100%; 
      flex-grow: 1;
      overflow-y: auto;
      border-bottom: 3px dashed #1e90ff; 
      border-radius: 12px 12px 0 0;
      background-color: #1a1d24;
      box-sizing: border-box;
      padding: 10px;
      color: #f5f5f5;
    ">
      """ + htmlm + """
    </div>

    <table style="width: 100%; border-collapse: collapse; background-color: #0c0f14;">
      <tr>
        <td style="width: 70%; padding: 5px;">
          <form action="/AI" method="POST" style="margin: 0;">
            <input 
              type="text" 
              name="query" 
              placeholder="Type your message..." 
              style="width: 95%; height: 40px; font-size: 16px; padding-left: 10px; border: 1px solid #444; border-radius: 6px; background-color: #11141a; color: #ffffff;">
        </td>
        <td style="width: 15%; text-align: right; padding: 5px;">
            <input 
              type="submit" 
              value="Send" 
              style="width: 90%; height: 40px; font-size: 15px; background-color: #1e90ff; color: white; border: none; border-radius: 6px; cursor: pointer;">
          </form>
        </td>

        <td style="width: 15%; text-align: right; padding: 5px;">
          <form action="/clear" method="POST" style="margin: 0;">
            <input 
              type="submit" 
              value="End Chat" 
              style="width: 90%; height: 40px; font-size: 15px; background-color: crimson; color: white; border: none; border-radius: 6px; cursor: pointer;">
          </form>
        </td>
      </tr>
    </table>

  </div>

  <script>
    window.onload = function() {
      var chatbox = document.getElementById("chatbox");
      if (chatbox) {
        chatbox.scrollTop = chatbox.scrollHeight;
      }
    };
  </script>

</body>
</html>



	"""


@app.route("/AI", methods=["POST"])
def AI():
    from collections import Counter

    with open("iframe.txt", "r") as file:
        htmlpage = file.read()

    query = request.form.get("query")
    query_embed = model.encode(query, convert_to_tensor=True)
    score = util.cos_sim(query_embed, questionbase_embed)
    answer = torch.argmax(score)
    with open("data.txt", "r", encoding="utf-8") as file:
      knowledgebase=file.readlines()
    final_ans=knowledgebase[answer]

    queryhtml = """<tr><td width ="50%"><div style="
      padding: 30px;
      font-size: 20px;
      background-color: #fafafa;
      border-top-left-radius: 15px;
      border-top-right-radius: 0;
      border-bottom-left-radius: 0;
      border-bottom-right-radius: 15px;
      font-size: 24px;
      color:black;
      border: 2px solid black;
      font-family: calibri;
      min-height: 100px;
      max-width: 300px;
    ">""" + query.title() + """</div></td><td width ="50%"></td></tr>"""

    html = """<tr><td width ="50%"></td><td width ="50%" align=right><div style="
      padding: 30px;
      font-size: 20px;
      background-color: #fafafa;
      border-top-left-radius: 15px;
      border-top-right-radius: 0;
      color:black;
      border-bottom-left-radius: 0;
      border-bottom-right-radius: 15px;
      font-size: 24px;
      border: 2px solid black;
      font-family: calibri;
      min-height: 100px;
      max-width: 300px;
    ">""" + final_ans + """</div></td></tr>"""

    htmlpage = htmlpage + """<table style='width:100%; padding:15px;'>""" + queryhtml + html + """</table>"""

    with open("iframe.txt", "w") as file:
        file.write(htmlpage)

    return redirect("/")


@app.route("/clear", methods=["POST"])
def clear():
	with open("iframe.txt", "w") as file:
		file.write("""<center><h1 style="font-family:calibri; color:#00ffff;">Ali's Chat Assistant</h1><br></center>""")
	return redirect("/")





@app.route("/admin", methods=["GET","POST"])
def admin():
	h="""<center><table width="60%" style="padding:15px; background-color:white; border-radius:15px;"><tr><td align=left><ol>"""
	with open("data.txt", "r", encoding="utf-8") as file:
		dashinfo = file.readlines()
	for line in dashinfo:
		h+="""<li style="font-size:28px; font-family:calibri;">"""+line+"</li><br>"
	h+="</ol></td></tr></table></center><br><br>"
	return"""

<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>Admin Panel</title>
</head>
<body bgcolor="#fff87a">
	<center><h1 style="font-family: calibri; color: #6e005b; font-size: 35px;">Feeded Information</h1></center><br>

	<center><table style="width:75%; height: 100px; background-color: white; border-radius: 28px; border: 3px dashed red;"><tr><td width="85%" style="padding-left: 20px;"><form method="POST" action="/addinfo"><input type="text" name="info" placeholder="Add New Info To KnowledgeBase" style="padding-left: 8px; width: 100%; border-left: none; border-right: none; border-top: none; border-bottom: 3px dashed royalblue; font-size: 17px; height: 45px;"><input type="text" name="qu" placeholder="Add Question Info To KnowledgeBase" style="padding-left: 8px; width: 100%; border-left: none; border-right: none; border-top: none; border-bottom: 3px dashed royalblue; font-size: 17px; height: 45px;"></td><td style="padding-right:15px;" width="15%" align="right"><input type="submit" value="Add Info" style="width: 80%; height: 45px; border: 3px dashed darkgoldenrod; border-radius: 8px; font-size: 17px; font-weight: bold; font-family: calibri; background-color: white;"></form></td></tr></table><br><br>"""+h+"""</center>

</body>
</html>




	"""

@app.route("/addinfo", methods=["POST"])
def addinfo():
    info = request.form.get("info")
    with open("data.txt", "a", encoding="utf-8") as file:
        file.write(info + "\n")

    question = request.form.get("qu")
    with open("question.txt", "a", encoding="utf-8") as file:
        file.write(question + "\n")

    return redirect("/admin")



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)