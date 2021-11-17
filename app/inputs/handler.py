import argparse

class handler:
    """
    Class to handle all the input variables and parsing passed to the main command.
    """
    args: argparse.Namespace
    arg_parser: argparse.ArgumentParser
    arg_parser_description: str = 'Amalgamate package reports across repos within an org and team to a single report'


    def parser(self):
        """
        Construct the argument parser object
        """

        self.arg_parser = argparse.ArgumentParser(description=self.arg_parser_description)

        org_group = self.arg_parser.add_argument_group("Orginisation details")
        org_group.add_argument('--organisation-slug',
                            help='Slug of org to use for permissions',
                            default= 'ministryofjustice',
                            required=True)
        org_group.add_argument('--organisation-token',
                            help='GitHub token which has org level access',
                            default='opg',
                            required=True)

        team_group = self.arg_parser.add_argument_group("Team options.")
        team_group.add_argument('--team-slug',
                            help='GitHub slug of the team to run against (can be a list, split by comma)',
                            required=True)
        return self

    def parse(self):
        """
        Parse & validate the input arguments.

        """
        args = self.arg_parser.parse_args()

        # no errors, so assign to self
        self.args = args
        return self
