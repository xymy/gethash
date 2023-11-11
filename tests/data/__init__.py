from pathlib import Path

DATA_DIR = Path(__file__).parent

FOO_TXT_NAME = "foo.txt"
FOO_TXT_PATH = DATA_DIR / "foo.txt"
FOO_TXT_SHA256_HASH = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
FOO_TXT_SHA256_HASH_LINE = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 *foo.txt\n"
FOO_TXT_SHA256_PATH = DATA_DIR / "foo.txt.sha256"
FOO_TXT_A_SHA256_PATH = DATA_DIR / "foo.txt.a.sha256"

FOO_ZIP_NAME = "foo.zip"
FOO_ZIP_PATH = DATA_DIR / "foo.zip"
FOO_ZIP_SHA256_HASH = "67e458e408a0e2da7f50b639d612f60e4c840e7175c7db707f22a9acc6df8427"
FOO_ZIP_SHA256_HASH_LINE = "67e458e408a0e2da7f50b639d612f60e4c840e7175c7db707f22a9acc6df8427 *foo.zip\n"
FOO_ZIP_SHA256_PATH = DATA_DIR / "foo.zip.sha256"
FOO_ZIP_A_SHA256_PATH = DATA_DIR / "foo.zip.a.sha256"
