import re
import xml.etree.ElementTree as ET
from typing import Protocol
from django.db import models


class FileLike(Protocol):
    def read(self) -> bytes: ...


class Doc(models.Model):
    """_summary_

    XML must confirm to the following general schema:

    ```xml
    <STANDARD>
       <META>
           <DOCUMENT.REF>
               <DATE>
           <PUBLICATION.REF>
               ...
               <LG.OJ>
               ...
           <SOURCE>
           <CELEX>
           <TITLE>
       <CONTENU>
           <TITRE>
           <PREAMBULE>
           <ARTICLES>
           <SIGNATURE>
       <ANNEXES>
           ...
    ```
    """

    DOCUMENT_REF_DATE = models.DateField()
    PUBLICATION_REF_FILE = models.CharField(max_length=50)
    PUBLICATION_REF_LG_OJ = models.CharField(max_length=3)
    SOURCE = models.CharField(max_length=6)
    # see https://eur-lex.europa.eu/content/help/eurlex-content/celex-number.html
    CELEX = models.CharField(max_length=11)
    CONTENU_TITRE = models.TextField()
    CONTENU_PREAMBULE = models.TextField()
    CONTENU_ARTICLES = models.TextField()
    CONTENU_SIGNATURE = models.TextField()
    ANNEXES = models.TextField()

    def __str__(self):
        return self.CELEX

    @classmethod
    def get_xml_text(cls, xml_str: str) -> str:
        """Extract the text content from an XML string.

        Args:
            xml_str (str): XML string.

        Returns:
            str: Extracted text.
        """
        # replace <NOTE></NOTE> tags by paranthesis
        text_str = re.sub("<NOTE.*?>", "(", xml_str)
        text_str = re.sub("</NOTE.*?>", ")", text_str)

        # drop all XML tags
        text_str = re.sub("<.*?>", "", text_str)

        # remove new line chars and repeated spaces
        text_str = re.sub(r"\s+", " ", text_str).strip()

        # remove spurious white spaces in front of punctuation
        text_str = re.sub(r"\s?([.,:;?)])", r"\1", text_str)

        return text_str

    @classmethod
    def map_xml_text_by_tag(cls, xml_document: str) -> dict:
        """Extract text from each element in an XML document and map it by tag name.

        This function takes an XML document as a string, parses it, and extracts the
        text content from each element. It then stores this information in a
        dictionary where the keys are the concatenated tag names of the elements in
        the XML tree and the values are the corresponding extracted text.

        Args:
            xml_str (str): _description_

        Returns:
            dict: _description_
        """
        # Extract doc's metadata
        standard = ET.fromstring(xml_document)

        doc_dict = dict()

        meta = standard.find("META")
        document_ref = meta.find("DOCUMENT.REF")
        doc_dict["DOCUMENT_REF_DATE"] = document_ref.find("DATE").text  # ISO date
        publ_ref = meta.find("PUBLICATION.REF")
        doc_dict["PUBLICATION_REF_FILE"] = publ_ref.attrib["FILE"]  # str
        doc_dict["PUBLICATION_REF_LG_OJ"] = publ_ref.find("LG.OJ").text  # str
        doc_dict["SOURCE"] = meta.find("SOURCE").text  # str
        doc_dict["CELEX"] = meta.find("CELEX").text  # str

        # Remove META element
        standard.remove(meta)

        # Extract doc's content
        contenu = standard.find("CONTENU")
        doc_dict["CONTENU_TITRE"] = cls.get_xml_text(
            ET.tostring(contenu.find("TITRE"), encoding="unicode")
        )
        doc_dict["CONTENU_PREAMBULE"] = cls.get_xml_text(
            ET.tostring(contenu.find("PREAMBULE"), encoding="unicode")
        )
        doc_dict["CONTENU_ARTICLES"] = cls.get_xml_text(
            ET.tostring(contenu.find("ARTICLES"), encoding="unicode")
        )
        doc_dict["CONTENU_SIGNATURE"] = cls.get_xml_text(
            ET.tostring(contenu.find("SIGNATURE"), encoding="unicode")
        )
        annexes = standard.find("ANNEXES")
        doc_dict["ANNEXES"] = cls.get_xml_text(ET.tostring(annexes, encoding="unicode"))

        return doc_dict

    @classmethod
    def from_xml(cls, file: FileLike):
        """Parse XML file, extract relevant data and save it to the database.

        Args:
            file (FileLike): Uploaded XML file.
        """
        # Read file with proper encoding
        bytes_str = file.read()
        encoding = "utf-8"
        if match_ := re.search(b"encoding=['\"](.*?)['\"]", bytes_str):
            encoding = match_.group(1).lower().decode()
        xml_str = bytes_str.decode(encoding)

        # parse xml content
        try:
            doc_dict = cls.map_xml_text_by_tag(xml_str)
        except Exception as e:
            raise Exception(
                "Invalid XML file. "
                "Check that the schema of the uploaded file corresponds to the schema "
                "expected by the API. "
                f"Exception details: {str(e)}"
            )

        # Save data to DB
        doc = cls(**doc_dict)
        doc.save()
