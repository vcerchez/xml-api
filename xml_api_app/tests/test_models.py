from xml_api_app.models import Doc


def test_get_xml_text():

    xml_str = """
        <TAG>
            <CHILD child_attr="foo"> child text
                <GRAND CHILD> <FORMAT>formatted text</FORMAT> plain text <NOTE>a note</NOTE>.
                </GRAND CHILD>
            </CHILD>
        </TAG>
    """
    expected = "child text formatted text plain text (a note)."

    text_str = Doc.get_xml_text(xml_str)

    assert text_str == expected


def test_map_xml_text_by_tag():

    expected = {
        "DOCUMENT_REF_DATE": "20240101",
        "PUBLICATION_REF_FILE": "file.xml",
        "PUBLICATION_REF_LG_OJ": "LAN",
        "SOURCE": "J_Name",
        "CELEX": "12345A6789",
        "CONTENU_TITRE": "Doc title.",
        "CONTENU_PREAMBULE": "Doc preambule.",
        "CONTENU_ARTICLES": "Doc articles.",
        "CONTENU_SIGNATURE": "Signed.",
        "ANNEXES": "Doc annexes.",
    }

    with open("xml_api_app/tests/test_case.xml", "rb") as file:
        xml_str = file.read().decode("utf-8")
    doc_dict = Doc.map_xml_text_by_tag(xml_str)

    assert doc_dict == expected
