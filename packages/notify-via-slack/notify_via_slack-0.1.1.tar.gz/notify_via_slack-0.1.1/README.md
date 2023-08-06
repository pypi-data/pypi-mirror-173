# Notify via slack

Install: `pip install notify-via-slack`

## Usage

Create an app in [slack api](https://api.slack.com/apps)

Save the bot token

Copy the .env.example to .env `cp .env.example .env`

Replace the `SLACK_BOT_TOKEN`

Send a message

```python
slack.notify import SlackNotify

handler = SlackNotify(app_name='My app name')
handler.notify(message='some message', emit_log=True, is_error=True)

```
