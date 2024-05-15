CONSTRAINT = 4  # change this to impose your desired constraint of attendance.


class GraduationCeremony:

    def __init__(self, days, constraint=4):
        """
        Instantiate GraduationCeremony class

        :param int days: number os days in an academic year.
        :param int constraint: not allowed to miss classes for four(default val) or more consecutive days.
        """
        if days < 0 or constraint < 0 or days < constraint:
            raise Exception(
                "Input provided is invalid. Check values for days and constraint.")
        self.days = days
        self.constraint = constraint

    # memoized solution
    def calculate_ways_of_attending(self, n, count, memo):
        """
        Constraint: You are not allowed to miss classes for four/self.constraint or more consecutive days.
        count keeps track of of how many days classes were missed consecutively.

        TIME COMPLEXITY: O(N*M){N=days|M=constraint}
        SPACE COMPLEXITY: O(N*M + N*M){N=days|M=constraint - space for memo + space for recursion stack}

        :param int n: days in academic year.
        :param int count: streak of absence.
        :param dict memo: storing solutions of overlapping sub-problems and reusing it.
        """
        if count == self.constraint:  # if count crosses defined constraint; its not a valid way of attending - return 0
            return 0

        if n == 0:  # if we have successfully attended classes until last day - its a valid way - return 1
            return 1

        if (n, count) in memo:
            return memo[(n, count)]

        # for a given day there are 2 option - either be present or absent
        # if 'absent': increment the count; move to next day
        # if 'present': streak of absence is lost; count re-initializes to 0
        absent = self.calculate_ways_of_attending(n-1, count+1, memo)
        present = self.calculate_ways_of_attending(n-1, 0, memo)

        memo[(n, count)] = absent + present
        return memo[(n, count)]

    # tabulation solution
    def calculate_ways_of_attending_tabulation(self):
        """
        Tabulation format of memoized solution.
        TIME COMPLEXITY: O(N*M){N=days|M=constraint}
        SPACE COMPLEXITY: O(N*M){N=days|M=constraint - space for dp table}
        """
        n = self.days
        count = self.constraint

        # count+1 & n+1 to manage index
        dp = [[0]*(count+1) for i in range(n+1)]

        for j in range(count):
            dp[0][j] = 1

        for i in range(1, n+1):
            for j in range(count-1, -1, -1):
                dp[i][j] = dp[i-1][j+1] + dp[i-1][0]

        total_ways_of_attending = dp[n][0]
        missing_class_on_last_day = dp[n-1][1]

        return f'{missing_class_on_last_day}/{total_ways_of_attending}'

    # tabulation solution with Space Optimization
    def calculate_ways_of_attending_tabulation_space_optimized(self):
        """
        Tabulation format of memoized solution with space optimization.
        TIME COMPLEXITY: O(N*M){N=days|M=constraint}
        SPACE COMPLEXITY: O(M){M=constraint - space for a single array}
        """
        n = self.days
        count = self.constraint

        # n+1 to manage index
        prev = [0]*(count+1)

        for j in range(count):
            prev[j] = 1

        for i in range(1, n+1):
            cur = [0]*(count+1)
            for j in range(count-1, -1, -1):
                cur[j] = prev[j+1] + prev[0]
            prev, cur = cur, prev

        total_ways_of_attending = prev[0]
        missing_class_on_last_day = cur[1]

        return f'{missing_class_on_last_day}/{total_ways_of_attending}'


def solution(n, constraint):
    """
    solution function to get the probability of missing the ceremony given the constraint.

    :param int n: days in academic year of university.
    :param int constraint: allowed to miss classes for four/constraint or more consecutive days.
    """

    graduation = GraduationCeremony(n, constraint)

    total_ways_of_attending = graduation.calculate_ways_of_attending(n, 0, {})
    missing_class_on_last_day = graduation.calculate_ways_of_attending(
        n-1, 1, {})  # last day - absent; count of absence streak initialized with 1
    print(
        f"Probability of missing graduation ceremony - [Memoized]: {missing_class_on_last_day}/{total_ways_of_attending}")
    print(
        f"Probability of missing graduation ceremony - [Tabulation]: {graduation.calculate_ways_of_attending_tabulation()}")
    print(
        f"Probability of missing graduation ceremony - [Tabulation with Space Optimization]: {graduation.calculate_ways_of_attending_tabulation_space_optimized()}")


if __name__ == '__main__':

    days = int(input("Enter number of days to attend classes: "))
    solution(days, constraint=CONSTRAINT)
