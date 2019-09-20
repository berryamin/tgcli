from datetime import datetime

import click
import colorful
import yaspin
import yaspin.spinners

import tgcli.request.bot


def _limit_validator(ctx, param, value: int):
    """
    Validates --limit option on "bot receive".
    """
    if value < 1 or value > 100:
        raise click.BadParameter('"limit" must be between 1-100.')

    return value


@click.command()
@click.option(
    "-l",
    "--limit",
    type=int,
    required=True,
    default=1,
    help="The limit for updates. Must be between 1-100. Defaults to 1.",
)
@click.pass_context
def receive(ctx, limit: int):
    session = tgcli.request.bot.BotSession(ctx.obj["token"])
    session.verify = ctx.obj["secure"]

    request = tgcli.request.bot.GetUpdatesRequest(session)

    with yaspin.yaspin(yaspin.spinners.Spinners.clock) as spinner:
        spinner.text = "Getting updates..."

        response = session.send(request)

        if response.ok:
            spinner.text = "Received updates."
            spinner.ok("✔️ ")

            data = response.json()["result"]

            for update in data:
                if "message" not in update:
                    pass

                message_obj = update["message"]

                message = message_obj["text"]
                date = datetime.utcfromtimestamp(message_obj["date"])
                sender = message_obj["from"].get(
                    "username", message_obj["from"]["id"]
                )

                out = "{c.bold}{sender} [{date}]:{c.reset}\t\t{message}".format(
                    c=colorful, sender=sender, date=date, message=message
                )
                print(out)
        else:
            data = response.json()

            code = data.get("error_code", "Unknown")
            description = data.get("description", "No description found.")
            spinner.write(
                "{c.bold_red}Error Code:{c.reset} {}".format(code, c=colorful)
            )
            spinner.write(
                "{c.bold_red}Error Details:{c.reset} {}".format(
                    description, c=colorful
                )
            )

            spinner.text = "Failed sending message."
            spinner.fail("❌")
            sys.exit(1)
