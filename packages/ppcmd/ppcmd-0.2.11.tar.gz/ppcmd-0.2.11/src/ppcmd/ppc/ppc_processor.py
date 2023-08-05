from ppcmd.common.print import print_major_cmd_step__


class PpcProcessor:

    def update(self):
        print_major_cmd_step__('update...')

    def test(self):
        print_major_cmd_step__('test...')

    def coverage(self):
        print_major_cmd_step__('coverage...')

    def lint(self):
        print_major_cmd_step__('lint...')
