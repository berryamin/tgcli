from click.testing import CliRunner

from tests.test_cli import (
    SKIPIF_BOT_RECEIVER_NOT_EXISTS,
    SKIPIF_BOT_TOKEN_NOT_EXISTS,
    SKIPIF_HAS_NOT_CONNECTED,
)


class TestReceiveMessage:
    @SKIPIF_HAS_NOT_CONNECTED
    @SKIPIF_BOT_TOKEN_NOT_EXISTS
    @SKIPIF_BOT_RECEIVER_NOT_EXISTS
    def test_vanilla(self, cli_runner: CliRunner, cli, receiver_id: str):
        args = ("bot", "receive")
        result = cli_runner.invoke(cli, args)
        assert result.exit_code == 0

    @SKIPIF_HAS_NOT_CONNECTED
    @SKIPIF_BOT_TOKEN_NOT_EXISTS
    @SKIPIF_BOT_RECEIVER_NOT_EXISTS
    def test_limit(self, cli_runner: CliRunner, cli, receiver_id: str):
        args = ("bot", "receive", "--limit", "2")
        result = cli_runner.invoke(cli, args)
        assert result.exit_code == 0
