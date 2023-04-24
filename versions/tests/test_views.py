import datetime

from model_bakery import baker


def test_version_list(version, logged_in_tp):
    """
    GET /versions/
    """
    res = logged_in_tp.get("version-list")
    logged_in_tp.response_200(res)


def test_version_list_context(version, old_version, inactive_version, logged_in_tp):
    """
    GET /versions/
    """
    older_version = baker.make(
        "versions.Version",
        name="Version 1.67.0",
        description="Sample",
        release_date=datetime.date.today() - datetime.timedelta(days=700),
    )
    res = logged_in_tp.get("version-list")
    logged_in_tp.response_200(res)
    assert "current_version" in res.context
    assert "version_list" in res.context
    assert len(res.context["version_list"]) == 2
    assert res.context["current_version"] == version
    assert old_version in res.context["version_list"]
    assert older_version in res.context["version_list"]
    assert old_version == res.context["version_list"][0]
    assert inactive_version not in res.context["version_list"]


def test_version_detail(version, logged_in_tp):
    """
    GET /versions/{slug}/
    """
    res = logged_in_tp.get("version-detail", slug=version.slug)
    logged_in_tp.response_200(res)
