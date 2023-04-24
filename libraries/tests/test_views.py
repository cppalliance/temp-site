import datetime

from model_bakery import baker


def test_library_list(library_version, logged_in_tp):
    """GET /libraries/"""
    last_year = datetime.date.today() - datetime.timedelta(days=365)
    v2 = baker.make("versions.Version", name="Version 1.78.0", release_date=last_year)
    lib2 = baker.make(
        "libraries.Library",
        name="sample",
    )
    baker.make("libraries.LibraryVersion", library=lib2, version=v2)
    res = logged_in_tp.get("libraries")
    logged_in_tp.response_200(res)
    assert "library_list" in res.context
    assert library_version.library in res.context["library_list"]
    assert lib2 not in res.context["library_list"]


def test_library_list_select_category(library, category, logged_in_tp):
    """POST /libraries/ to submit a category redirects to the libraries-by-category page"""
    res = logged_in_tp.post("libraries", data={"categories": category.pk})
    logged_in_tp.response_302(res)
    assert res.url == f"/libraries-by-category/{category.slug}/"


def test_library_list_by_category(library_version, category, logged_in_tp):
    """GET /libraries-by-category/{category_slug}/"""
    library = library_version.library
    baker.make("libraries.Library", name="Sample")
    library.categories.add(category)
    res = logged_in_tp.get("libraries-by-category", category.slug)
    logged_in_tp.response_200(res)
    assert "library_list" in res.context
    assert len(res.context["library_list"]) == 1
    assert library in res.context["library_list"]
    assert "category" in res.context
    assert res.context["category"] == category


def test_library_list_by_category_no_results(library_version, category, logged_in_tp):
    """
    GET /libraries-by-category/{category_slug}/
    A category with no libraries
    """
    res = logged_in_tp.get("libraries-by-category", category.slug)
    logged_in_tp.response_200(res)
    assert "library_list" in res.context
    assert len(res.context["library_list"]) == 0


def test_library_list_by_category_no_results_for_active_version(
    library, category, logged_in_tp
):
    """
    GET /libraries-by-category/{category_slug}/
    A category with a library, but the library isn't attached to the active Boost version
    """
    res = logged_in_tp.get("libraries-by-category", category.slug)
    logged_in_tp.response_200(res)
    assert "library_list" in res.context
    assert len(res.context["library_list"]) == 0


def test_libraries_by_category(logged_in_tp, library, category):
    """GET /libraries-by-category/{slug}/"""
    baker.make("libraries.Library", name="Sample")
    library.categories.add(category)
    res = logged_in_tp.get("libraries-by-category", category.slug)
    logged_in_tp.response_200(res)
    assert "library_list" in res.context
    assert len(res.context["library_list"]) == 1
    assert library in res.context["library_list"]
    assert "category" in res.context
    assert res.context["category"] == category


def test_library_detail(library_version, logged_in_tp):
    """GET /libraries/{slug}/"""
    library = library_version.library
    url = logged_in_tp.reverse("library-detail", library.slug)
    response = logged_in_tp.get(url)
    logged_in_tp.response_200(response)


def test_library_detail_404(library, logged_in_tp):
    """GET /libraries/{slug}/"""
    # 404 due to bad slug
    url = logged_in_tp.reverse("library-detail", "bananas")
    response = logged_in_tp.get(url)
    logged_in_tp.response_404(response)

    # 404 due to no existing version
    url = logged_in_tp.reverse("library-detail", library.slug)
    response = logged_in_tp.get(url)
    logged_in_tp.response_404(response)


def test_library_detail_context_get_closed_prs_count(logged_in_tp, library_version):
    """
    GET /libraries/{slug}/
    Test that the custom closed_prs_count var appears as expected
    """
    library = library_version.library
    # Create open and closed PRs for this library, and another random PR
    lib2 = baker.make("libraries.Library", slug="sample")
    baker.make("libraries.PullRequest", library=library, is_open=True)
    baker.make("libraries.PullRequest", library=library, is_open=False)
    baker.make("libraries.PullRequest", library=lib2, is_open=True)
    url = logged_in_tp.reverse("library-detail", library.slug)
    response = logged_in_tp.get(url)
    logged_in_tp.response_200(response)
    assert "closed_prs_count" in response.context
    # Verify that the count only includes the one open PR for this library
    assert response.context["closed_prs_count"] == 1


def test_library_detail_context_get_maintainers(logged_in_tp, user, library_version):
    """
    GET /libraries/{slug}/
    Test that the maintainers var appears as expected
    """
    library_version.maintainers.add(user)
    library = library_version.library
    # Create open and closed PRs for this library, and another random PR
    lib2 = baker.make("libraries.Library", slug="sample")
    baker.make("libraries.PullRequest", library=library, is_open=True)
    baker.make("libraries.PullRequest", library=library, is_open=False)
    baker.make("libraries.PullRequest", library=lib2, is_open=True)
    url = logged_in_tp.reverse("library-detail", library.slug)
    response = logged_in_tp.get(url)
    logged_in_tp.response_200(response)
    assert "maintainers" in response.context
    assert len(response.context["maintainers"]) == 1
    assert response.context["maintainers"][0] == user


def test_library_detail_context_get_open_issues_count(logged_in_tp, library_version):
    """
    GET /libraries/{slug}/
    Test that the custom open_issues_count var appears as expected
    """
    library = library_version.library
    # Create open and closed issues for this library, and another random issue
    lib2 = baker.make("libraries.Library", slug="sample")
    baker.make("libraries.Issue", library=library, is_open=True)
    baker.make("libraries.Issue", library=library, is_open=False)
    baker.make("libraries.Issue", library=lib2, is_open=True)
    url = logged_in_tp.reverse("library-detail", library.slug)
    response = logged_in_tp.get(url)
    logged_in_tp.response_200(response)
    assert "open_issues_count" in response.context
    # Verify that the count only includes the one open issue for this library
    assert response.context["open_issues_count"] == 1


def test_libraries_by_version_by_category(logged_in_tp, library_version, category):
    """GET /libraries-by-category/{slug}/"""
    library = library_version.library
    version = library_version.version

    baker.make("libraries.Library", name="Sample")
    library.categories.add(category)
    res = logged_in_tp.get(
        "libraries-by-version-by-category", version.slug, category.slug
    )
    logged_in_tp.response_200(res)
    assert "library_list" in res.context
    assert len(res.context["library_list"]) == 1
    assert library in res.context["library_list"]
    assert "category" in res.context
    assert res.context["category"] == category


def test_libraries_by_version_list(logged_in_tp, library_version):
    """GET /versions/{version_slug}/libraries/"""
    # Create a new library_version
    excluded_library = baker.make("libraries.Library", name="Sample")
    res = logged_in_tp.get("libraries-by-version", library_version.version.slug)
    logged_in_tp.response_200(res)
    assert "library_list" in res.context

    # Confirm that correct libraries are present
    assert len(res.context["library_list"]) == 1
    assert library_version.library in res.context["library_list"]
    assert excluded_library not in res.context["library_list"]


def test_libraries_by_version_detail(logged_in_tp, library_version):
    """GET /versions/{version_slug}/libraries/{slug}/"""
    res = logged_in_tp.get(
        "library-detail-by-version",
        library_version.version.slug,
        library_version.library.slug,
    )
    logged_in_tp.response_200(res)
    assert "version" in res.context


def test_libraries_by_version_detail_no_library_found(logged_in_tp, library_version):
    """GET /versions/{version_slug}/{slug}/"""
    res = logged_in_tp.get(
        "libraries-detail-by-version",
        library_version.version.slug,
        "coffee",
    )
    logged_in_tp.response_404(res)


def test_libraries_by_version_detail_no_version_found(logged_in_tp, library_version):
    """GET /versions/{version_slug}/{slug}/"""
    res = logged_in_tp.get(
        "libraries-detail-by-version",
        0000,
        library_version.library.slug,
    )
    logged_in_tp.response_404(res)


def test_libraries_by_version_list_select_category(
    library_version, category, logged_in_tp
):
    """POST versions/{version_slug}/libraries/ to submit a category redirects to the libraries-by-category page"""
    version = library_version.version
    url = logged_in_tp.reverse("libraries-by-version", version.slug)
    res = logged_in_tp.post(url, data={"categories": category.pk})
    logged_in_tp.response_302(res)
    assert res.url == f"/versions/{version.slug}/libraries-by-category/{category.slug}/"
