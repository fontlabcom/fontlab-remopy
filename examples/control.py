# this_file: examples/control.py
# SPDX-License-Identifier: Apache-2.0
"""Ordinary external Python using the public FontLab client export.

The implementation lives in fontlab_remopy.client; public imports stay stable.
"""

from fontlab_remopy import FontLab


def main() -> None:
    with FontLab() as fl:
        print(fl.fonts())
        print(fl.eval('[font["family_name"] for font in fontpr.list_fonts()["fonts"]]'))
        completed = fl.run(
            "print(message); result={'length':len(message)}", message="Łódź"
        )
        print(completed.value, completed.stdout)

        @fl.python
        def native_summary() -> dict:
            import fontpr

            return {"fonts": fontpr.list_fonts(), "glyphs": fontpr.get_current_glyphs()}

        print(native_summary())


if __name__ == "__main__":
    main()
