import resend

resend.api_key = "re_7fZvmRvA_GNTaKYjxbM8R1CEfsasSknWj"

params: resend.Emails.SendParams = {
  "from": "reddit search <noreply@solobuilderhub.com>",
  "to": ["omifarhan@gmail.com"],
  "subject": "We have found a post with your keyword!",
  "html": "<p>it works!</p>"
}

email = resend.Emails.send(params)
print(email)