import unittest
from unittest.mock import Mock, patch

from sikriml_core.models.ner import ScoreEntity, ScoreLabel
from sikriml_ner_rule import RuleProcessor
from sikriml_ner_rule.handlers import EntityHandler


class RuleProcessorTest(unittest.TestCase):
    @patch(
        "sikriml_ner_rule.handlers.EntityHandler.__abstractmethods__",
        set(),
    )
    def test_process_correct_result(self):
        # Arrange
        number = "123"
        text = "Text with {number}"
        expected_entity = set([ScoreEntity(number, 10, 13, ScoreLabel.NUMB)])
        number_handler = EntityHandler()
        number_handler.process = Mock(return_value=expected_entity)
        processor = RuleProcessor([number_handler])
        # Act
        result = processor.process(text)
        # Assert
        self.assertSetEqual(result, expected_entity)


if __name__ == "__main__":
    unittest.main(verbosity=2)
