from pathlib import Path

from pptlint import cli


def test_parse_args():
    args = cli._parse_args(["deck.pptx", "--report", "out.md"])

    assert args.pptx == "deck.pptx"
    assert args.report == "out.md"


def test_main_success(monkeypatch, capsys, tmp_path):
    called = {}

    def fake_load(p):
        called["path"] = p
        return object()

    class FakeAnalyzer:
        def analyze(self, pres):
            called["analyzed"] = pres
            return [{"category": "X", "message": "ok", "slide": 1}]

    def fake_print_report(issues):
        called["printed"] = issues

    def fake_write_report(issues, path):
        called["markdown"] = (issues, path)

    report_path = tmp_path / "report.md"

    monkeypatch.setattr(cli, "load_presentation", fake_load)
    monkeypatch.setattr(cli, "PresentationAnalyzer", FakeAnalyzer)
    monkeypatch.setattr(cli, "print_report", fake_print_report)
    monkeypatch.setattr(cli, "write_markdown_report", fake_write_report)

    rc = cli.main(["deck.pptx", "--report", str(report_path)])
    out = capsys.readouterr().out

    assert rc == 0
    assert called["path"] == Path("deck.pptx")
    assert "Файл: deck.pptx" in out
    assert called["markdown"][1] == str(report_path)


def test_main_error(monkeypatch, capsys):
    def fake_load(_):
        raise RuntimeError("boom")

    monkeypatch.setattr(cli, "load_presentation", fake_load)

    rc = cli.main(["deck.pptx"])
    err = capsys.readouterr().err

    assert rc == 1
    assert "Ошибка: boom" in err