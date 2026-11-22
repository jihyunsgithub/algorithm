#include <vector>
#include <algorithm>
using namespace std;

int solution(vector<vector<int>> sticker, vector<vector<int>> target)
{
    int N = sticker.size();
    int M = sticker[0].size();

    int totalOne = 0;
    int maxWrong = 0;

    for (int r = 0; r < N; r++) {
        int one = 0;
        int zero = 0;

        for (int c = 0; c < M; c++) {
            if (sticker[r][c] != target[r][c]) {
                if (sticker[r][c] == 1)
                    one++;
                else
                    zero++;
            }
        }

        totalOne += one;
        maxWrong = max(maxWrong, one + zero);
    }

    return max(totalOne, maxWrong);
}