import resend
from model import SendEmail, EmailRedditPost
import os
from jinja2 import Environment, FileSystemLoader


class EmailService:
    
    def __init__(self, email_details: SendEmail):
        self.email_details = email_details
        self.api_key = os.getenv("RESEND_API_KEY")
        self.env = Environment(loader=FileSystemLoader('.'))
        resend.api_key = self.api_key

    def truncate_text(self, text, char_limit=100):
      if len(text) > char_limit:
          return text[:char_limit] + '...'
      return text
    
    def build_params(self):
        template = self.env.get_template('email_template.html')
        # Truncate post texts
        for post in self.email_details.posts:
            post.text = self.truncate_text(post.text)

        email_content = template.render(posts=self.email_details.posts)

        params = resend.Emails.SendParams = { 
            "from" : "reddit search <noreply@solobuilderhub.com>",
            "to" : [self.email_details.email],
            "subject" : "We have found Reddit posts with your keyword!",
            "html": email_content
        }
        return params
    
    def send_email(self):
        try:
            params = self.build_params()
            email = resend.Emails.send(params)
        except Exception as e:
            raise e
    






# Example usage
if __name__ == "__main__":
    posts = [
        EmailRedditPost(url="https://reddit.com/r/example1", text="Example text 1", title="Example title 1", keyword="example", subreddit="r/example1"),
        EmailRedditPost(url="https://reddit.com/r/example2", text="Example text 2", title="Example title 2", keyword="example", subreddit="r/example2"),
    ]
    send_email = SendEmail(email="omifarhan@gmail.com", posts=posts)
    email_service = EmailService(send_email)
    response = email_service.send_email()
    print(response)

