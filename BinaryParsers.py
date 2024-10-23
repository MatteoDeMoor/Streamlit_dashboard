# binary_parsers.py

class BinaryPaq2018Helper:
    BITVECTOR_BYTE_SIZE = 4
    NUMBER_OF_BYTES = 12  # Each item uses 12 bytes (3 * 4 bytes)
    CHAR_SIMPLIFY_OFFSET = 64  # For character conversion (A=65 in ASCII)

    def __init__(self, paq2018_answers):
        self.paq2018_answers = paq2018_answers
        self.total_items = int(len(self.paq2018_answers) / self.NUMBER_OF_BYTES)

    def parse_item(self, item_index):
        if item_index < 1 or item_index > self.total_items:
            raise ValueError(f"Item index {item_index} out of range.")

        # Calculate offset
        offset = (item_index - 1) * self.NUMBER_OF_BYTES
        item_bytes = self.paq2018_answers[offset:offset + self.NUMBER_OF_BYTES]
        if len(item_bytes) < self.NUMBER_OF_BYTES:
            raise ValueError(f"Not enough data for item index {item_index}.")

        # Read the three 4-byte integers
        left_statement_int = int.from_bytes(item_bytes[0:4], byteorder='little')
        right_statement_int = int.from_bytes(item_bytes[4:8], byteorder='little')
        value_int = int.from_bytes(item_bytes[8:12], byteorder='little')

        # Parse statements and value
        code_left_statement = self.get_statement_from_int(left_statement_int)
        code_right_statement = self.get_statement_from_int(right_statement_int)
        is_inversed = bool((value_int >> 0) & 0x1)  # inversedBitSector (1 bit)
        normative_value = (value_int >> 1) & 0x7  # answerBitSector (3 bits)

        return {
            "ItemIndex": item_index,
            "LeftStatement": code_left_statement,
            "RightStatement": code_right_statement,
            "IsInversed": is_inversed,
            "Answer": normative_value
        }

    def get_statement_from_int(self, value_int):
        # Extract bits
        nonNumeric1 = (value_int >> 0) & 0x1F  # bits 0-4 (5 bits)
        nonNumeric2 = (value_int >> 5) & 0x1F  # bits 5-9 (5 bits)
        nonNumeric3 = (value_int >> 10) & 0x1F  # bits 10-14 (5 bits)
        numeric = (value_int >> 15) & 0x7F  # bits 15-21 (7 bits)
        nonNumeric1Part2 = (value_int >> 22) & 0x1F  # bits 22-26 (5 bits)

        # Convert to characters
        chars = []
        chars.append(chr(nonNumeric1 + self.CHAR_SIMPLIFY_OFFSET))
        chars.append(chr(nonNumeric2 + self.CHAR_SIMPLIFY_OFFSET))
        chars.append(chr(nonNumeric3 + self.CHAR_SIMPLIFY_OFFSET))

        nonNumericCodePart = ''.join(chars)
        numericCodePart = f"{numeric:02d}"

        if nonNumeric1Part2 != 0:
            # There's a second non-numeric part
            chars2 = []
            chars2.append(chr(nonNumeric1Part2 + self.CHAR_SIMPLIFY_OFFSET))
            nonNumericCodePart2 = ''.join(chars2)
            return f"{nonNumericCodePart}_{numericCodePart}_{nonNumericCodePart2}"
        else:
            return f"{nonNumericCodePart}_{numericCodePart}"


class BinaryFcaHelper:
    BITVECTOR_BYTE_SIZE = 4
    NUMBER_OF_BYTES = 16  # Number of bytes reserved for one item (128 bits)

    def __init__(self, fca_answers):
        self.fca_answers = fca_answers
        self.total_items = int(len(self.fca_answers) / self.NUMBER_OF_BYTES)

    def parse_item(self, question_index):
        if question_index < 1 or question_index > self.total_items:
            raise ValueError(f"Question index {question_index} out of range.")

        # Get the bytes for the question index
        offset = (question_index - 1) * self.NUMBER_OF_BYTES
        item_bytes = self.fca_answers[offset:offset + self.NUMBER_OF_BYTES]

        if len(item_bytes) < self.NUMBER_OF_BYTES:
            raise ValueError(f"Not enough data for question index {question_index}.")

        # Get binary string
        bits = self.get_binary_string_from_bytes(item_bytes)

        # Extract values
        item_id = self.get_value_from_binary_string(bits, 0, 20)
        if item_id == 0:
            return None  # Termination condition

        sequence_ids = [
            self.get_value_from_binary_string(bits, 20, 3),
            self.get_value_from_binary_string(bits, 23, 3),
            self.get_value_from_binary_string(bits, 26, 3)
        ]
        # Adjust SequenceIds
        sequence_ids = [
            sid if sid != 0 else idx + 1
            for idx, sid in enumerate(sequence_ids)
        ]

        answers = [
            self.get_value_from_binary_string(bits, 29, 3),
            self.get_value_from_binary_string(bits, 32, 3),
            self.get_value_from_binary_string(bits, 35, 3)
        ]

        # Parse Competencies and their Correct Answers
        competencies = []
        competency_positions = [
            (38, 48),   # Competency 1 start positions
            (57, 67),   # Competency 2 start positions
            (76, 86),   # Competency 3 start positions
            (95, 105)   # Competency 4 start positions
        ]

        for idx, (comp_start, corr_start) in enumerate(competency_positions):
            competency_id = self.get_value_from_binary_string(bits, comp_start, 10)
            if competency_id != 0:
                correct_answers = [
                    self.get_value_from_binary_string(bits, corr_start, 3),
                    self.get_value_from_binary_string(bits, corr_start + 3, 3),
                    self.get_value_from_binary_string(bits, corr_start + 6, 3)
                ]
                competencies.append({
                    'CompetencyId': competency_id,
                    'CorrectAnswers': correct_answers
                })

        time_spent = self.get_value_from_binary_string(bits, 114, 14)

        return {
            "QuestionIndex": question_index,
            "ItemId": item_id,
            "SequenceIds": sequence_ids,
            "Answers": answers,
            "Competencies": competencies,
            "TimeSpent": time_spent
        }

    def get_binary_string_from_bytes(self, bytes_list):
        # Convert bytes to binary string
        return ''.join(f'{byte:08b}' for byte in bytes_list)

    def get_value_from_binary_string(self, bits, start_index, length):
        # Extract integer value from binary string
        return int(bits[start_index:start_index + length], 2)


class BinaryBaqHelper:
    BITVECTOR_BYTE_SIZE = 4
    NUMBER_OF_BYTES = 8  # Number of bytes per item

    # Define the bit masks and shifts
    ITEM_ID_MASK = 0x3F  # 6 bits for ItemId (bits 0-5)
    VALUE_MASK = 0xF     # 4 bits for each value (bits 6-9, 10-13, etc.)
    VALUE_SHIFTS = [6, 10, 14, 18, 22]  # Bit positions for the five values

    def __init__(self, baq_answers):
        self.baq_answers = baq_answers
        self.total_items = int(len(self.baq_answers) / self.NUMBER_OF_BYTES)

    def parse_item(self, item_index):
        if item_index < 1 or item_index > self.total_items:
            raise ValueError(f"Item index {item_index} out of range.")

        offset = (item_index - 1) * self.NUMBER_OF_BYTES

        if offset + self.NUMBER_OF_BYTES > len(self.baq_answers):
            raise ValueError(f"Not enough data for item index {item_index}.")

        item_bytes = self.baq_answers[offset:offset + self.NUMBER_OF_BYTES]

        normative_bytes = item_bytes[:self.BITVECTOR_BYTE_SIZE]
        ipsative_bytes = item_bytes[self.BITVECTOR_BYTE_SIZE:]

        normative = int.from_bytes(normative_bytes, byteorder='little')
        ipsative = int.from_bytes(ipsative_bytes, byteorder='little')

        # Extract ItemId from both normative and ipsative data
        item_id = self.extract_item_id(normative)
        ipsative_item_id = self.extract_item_id(ipsative)

        # Check if ItemIds match
        if item_id != ipsative_item_id:
            print(f"Warning: ItemId mismatch at item index {item_index}")

        # Extract NormativeValues and IpsativeValues
        normative_values = self.extract_values(normative)
        ipsative_values = self.extract_values(ipsative)

        return {
            "ItemIndex": item_index,
            "ItemId": item_id,
            "NormativeValues": normative_values,
            "IpsativeValues": ipsative_values
        }

    def extract_item_id(self, value):
        return value & self.ITEM_ID_MASK

    def extract_values(self, value):
        values = []
        for shift in self.VALUE_SHIFTS:
            val = (value >> shift) & self.VALUE_MASK
            values.append(val)
        return values


class BinarySjtHelper:
    NUMBER_OF_BYTES = 8  # Number of bytes per item

    def __init__(self, sjt_answers):
        self.sjt_answers = sjt_answers
        self.total_items = int(len(self.sjt_answers) / self.NUMBER_OF_BYTES)

    def parse_item(self, item_index):
        if item_index < 1 or item_index > self.total_items:
            raise ValueError(f"Item index {item_index} out of range.")

        # Get the bytes for the question index
        offset = (item_index - 1) * self.NUMBER_OF_BYTES
        item_bytes = self.sjt_answers[offset:offset + self.NUMBER_OF_BYTES]

        if len(item_bytes) < self.NUMBER_OF_BYTES:
            raise ValueError(f"Not enough data for item index {item_index}.")

        # Get binary string
        bits = self.get_binary_string(item_bytes)

        # Extract values
        situation_id = self.get_value_from_binary_string(bits, 0, 20)
        if situation_id == 0:
            return None  # Termination condition

        sequence_ids = [
            self.get_value_from_binary_string(bits, 20, 4),
            self.get_value_from_binary_string(bits, 24, 4),
            self.get_value_from_binary_string(bits, 28, 4)
        ]
        # Adjust SequenceIds
        sequence_ids = [
            sid if sid != 0 else idx + 1
            for idx, sid in enumerate(sequence_ids)
        ]

        answers = [
            self.get_value_from_binary_string(bits, 32, 3),
            self.get_value_from_binary_string(bits, 35, 3),
            self.get_value_from_binary_string(bits, 38, 3)
        ]

        scores = [
            self.get_value_from_binary_string(bits, 41, 3),
            self.get_value_from_binary_string(bits, 44, 3),
            self.get_value_from_binary_string(bits, 47, 3)
        ]

        time_spent = self.get_value_from_binary_string(bits, 50, 14)

        return {
            "ItemIndex": item_index,
            "SituationId": situation_id,
            "SequenceIds": sequence_ids,
            "Answers": answers,
            "Scores": scores,
            "TimeSpent": time_spent
        }

    def get_binary_string(self, bytes_list):
        # Convert bytes to binary string
        return ''.join(f'{byte:08b}' for byte in bytes_list)

    def get_value_from_binary_string(self, bits, start_index, length):
        # Extract integer value from binary string
        return int(bits[start_index:start_index + length], 2)

class BinaryRatHelper:
    def __init__(self, assessment_model_config_code, rat_answers, is_nrat=False):
        self.TestId = assessment_model_config_code
        self.rat_answers = rat_answers
        self.is_nrat = is_nrat

        if self.is_nrat:
            self.NUMBER_OF_BYTES = 12  # 12 bytes per item for NRAT
        else:
            self.NUMBER_OF_BYTES = 8   # 8 bytes per item for RAT

        self.total_items = int(len(self.rat_answers) / self.NUMBER_OF_BYTES)

    def parse_item(self, question_index):
        if question_index < 1 or question_index > self.total_items:
            raise ValueError(f"Question index {question_index} out of range.")

        offset = (question_index - 1) * self.NUMBER_OF_BYTES
        item_bytes = self.rat_answers[offset:offset + self.NUMBER_OF_BYTES]

        if len(item_bytes) < self.NUMBER_OF_BYTES:
            raise ValueError(f"Not enough data for question index {question_index}.")

        if not self.is_nrat:
            # RAT Parsing Logic
            definition_bytes = item_bytes[:4]
            value_bytes = item_bytes[4:]

            # Convert bytes to integers (little-endian)
            definition = int.from_bytes(definition_bytes, byteorder='little')
            value = int.from_bytes(value_bytes, byteorder='little')

            # Extract fields from definition bit vector
            screen_id = (definition >> 0) & 0x7FFF  # 15 bits (bits 0-14)
            clone_id = (definition >> 15) & 0xFF    # 8 bits (bits 15-22)
            item_id = (definition >> 23) & 0xFF     # 8 bits (bits 23-30)

            # Extract fields from value bit vector
            answer = (value >> 0) & 0xF             # 4 bits (bits 0-3)
            correct_answer = (value >> 4) & 0xF     # 4 bits (bits 4-7)
            time_spent = (value >> 8) & 0xFFF       # 12 bits (bits 8-19)
            is_answered = (value >> 20) & 0x1       # 1 bit (bit 20)

            is_empty = item_id == 0

            if is_empty:
                return None  # Termination condition

            question_code = f"{self.TestId}_S{str(screen_id).zfill(4)}_C{str(clone_id).zfill(2)}_Q{str(item_id).zfill(2)}"

            return {
                "QuestionIndex": question_index,
                "QuestionCode": question_code,
                "ScreenId": screen_id,
                "CloneId": clone_id,
                "ItemId": item_id,
                "Answer": answer,
                "CorrectAnswer": correct_answer,
                "TimeSpent": time_spent,
                "IsAnswered": bool(is_answered),
                "IsEmpty": is_empty
            }

        else:
            # NRAT Parsing Logic
            screen_definition_bytes = item_bytes[:4]
            item_definition_bytes = item_bytes[4:8]
            value_bytes = item_bytes[8:]

            # Convert bytes to integers (little-endian)
            screen_definition = int.from_bytes(screen_definition_bytes, byteorder='little')
            item_definition = int.from_bytes(item_definition_bytes, byteorder='little')
            value = int.from_bytes(value_bytes, byteorder='little')

            # Extract fields from screen definition bit vector
            screen_id = (screen_definition >> 0) & 0x7FFF     # 15 bits (bits 0-14)
            clone_id = (screen_definition >> 15) & 0x7FFF     # 15 bits (bits 15-29)

            # Extract fields from item definition bit vector
            item_id = (item_definition >> 0) & 0x7FFF         # 15 bits (bits 0-14)
            item_clone_id = (item_definition >> 15) & 0x7FFF  # 15 bits (bits 15-29)

            # Extract fields from value bit vector
            answer = (value >> 0) & 0xF             # 4 bits (bits 0-3)
            correct_answer = (value >> 4) & 0xF     # 4 bits (bits 4-7)
            time_spent = (value >> 8) & 0xFFF       # 12 bits (bits 8-19)
            is_answered = (value >> 20) & 0x1       # 1 bit (bit 20)

            is_empty = item_id == 0

            if is_empty:
                return None  # Termination condition

            question_code = f"{self.TestId}_S{str(screen_id).zfill(4)}_C{str(clone_id).zfill(2)}_Q{str(item_id).zfill(2)}_C{str(item_clone_id).zfill(2)}"

            return {
                "QuestionIndex": question_index,
                "QuestionCode": question_code,
                "ScreenId": screen_id,
                "CloneId": clone_id,
                "ItemId": item_id,
                "ItemCloneId": item_clone_id,
                "Answer": answer,
                "CorrectAnswer": correct_answer,
                "TimeSpent": time_spent,
                "IsAnswered": bool(is_answered),
                "IsEmpty": is_empty
            }

class BinaryMdqRegulationHelper:
    BITVECTOR_BYTE_SIZE = 4
    NUMBER_OF_BYTES = 8  # Number of bytes reserved for one item

    def __init__(self, mdq_answers):
        self.mdq_answers = mdq_answers
        self.total_items = int(len(self.mdq_answers) / self.NUMBER_OF_BYTES)

    def parse_item(self, item_index):
        if item_index < 1 or item_index > self.total_items:
            raise ValueError(f"Item index {item_index} out of range.")

        # Get the bytes for the item index
        offset = (item_index - 1) * self.NUMBER_OF_BYTES
        item_bytes = self.mdq_answers[offset:offset + self.NUMBER_OF_BYTES]

        if len(item_bytes) < self.NUMBER_OF_BYTES:
            raise ValueError(f"Not enough data for item index {item_index}.")

        # Convert bytes to integers
        normative = int.from_bytes(item_bytes[:self.BITVECTOR_BYTE_SIZE], byteorder='little')
        ipsative = int.from_bytes(item_bytes[self.BITVECTOR_BYTE_SIZE:], byteorder='little')

        item_id = self.extract_item_id(normative)
        normative_values = self.extract_values(normative)
        ipsative_values = self.extract_values(ipsative)

        # Check for termination condition (all zeros)
        if item_id == 0 and all(value == 0 for value in normative_values) and all(value == 0 for value in ipsative_values):
            return None  # Termination condition

        return {
            "ItemIndex": item_index,
            "ItemId": item_id,
            "NormativeValues": normative_values,
            "IpsativeValues": ipsative_values
        }

    def extract_item_id(self, value):
        return (value >> 0) & 0x3F  # 6 bits for ItemId

    def extract_values(self, value):
        value_masks = [0x7, 0x7, 0x7, 0x7, 0x7, 0x7]
        value_shifts = [6, 9, 12, 15, 18, 21]
        values = [(value >> shift) & mask for shift, mask in zip(value_shifts, value_masks)]
        return values