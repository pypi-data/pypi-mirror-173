"""

    petdataset.py


    this file contains the petdataset class, an interface to the PETdataset hosted on huggingface.


    status: under development
"""

from datasets import load_dataset

class PETdataset:

    def __init__(self):
        self.dataset = load_dataset("patriziobellan/PET", name='relations-extraction')

    def __len__(self):
        """the length of a RelationsExtraction instance is equal to the number of documents of the dataset

        Returns:
            the number of document of the PET dataset.

        """
        return len(self.dataset['test']['document name'])


    def GetDocument(self, document_identifier: Union[int, str]) -> str:
        """Get the document's text of a given text identifier.

        Example::

            Get the document text providing document number.

            >>> pet = RelationsExtraction()

            >>> text1 = pet.GetDocument(1)

            >>> print(text1)

            Get the document text providing document name.

            >>> text1 = pet.GetDocument('doc-1.1')

            >>> print(text1)

        Args

            document_identifier (int): the number of the document you want the text.
            document_identifier (str): the name of the document you want the text.

        Returns:

            str: the document text.

        """
        if type(document_identifier) == int:

            return ' '.join(self.dataset['test']['tokens'][document_identifier]).strip()

        elif type(document_identifier) == str:
            document_identifier = self.GetDocumentNumber(document_identifier)

            return ' '.join(self.dataset['test']['tokens'][document_identifier]).strip()

    def GetDocumentName(self, document_number: int) -> str:
        """Get the document name of a given numeric identifier document_number.

        Args:
            document_number (int): the document number.

        Returns:
            the document name of a given document_number.

        """

        return self.dataset['test']['document name'][document_number]

    def GetDocumentNumber(self, document_name: str) -> int:
        """Get the document id of a given document name.

        Args:
            document_name (str): the name of the document.

        Returns (str):
            the document number (a.k.a. Id).

        """

        docs = {self.dataset['test'][n_]['document name']: n_ for n_ in range(len(self.dataset['test']))}

        return docs[document_name]

    def GetDocumentNames(self) -> list:
        """Get the list of documents' name.

        Returns:
            list of documents name

        """

        return list(set(self.dataset['test']['document name']))

    ########################
    #
    ########################

    @staticmethod
    def _remove_B_I_prefix(tag_label):
        #  remove the prefix B/I from tag label
        if len(tag_label) == 1:
            return tag_label
        else:
            return tag_label[2:]
