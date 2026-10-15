"""Generate the browser fixture through real local APIs on synthetic bytes only."""
import json
from tools.scientific_transients.test_derived_preparation import PreparationFixture


def main():
    fixture=PreparationFixture()
    try:
        fixture.setUp()
        print(json.dumps(fixture.payload(),sort_keys=True,separators=(',',':')))
    finally:
        fixture.doCleanups()


if __name__=='__main__':main()
