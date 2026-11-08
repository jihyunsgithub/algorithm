#include <vector>
#include <queue>

using namespace std;

int solution(vector<vector<int> > board) {
    int n = board.size();
    int m = board[0].size();
    vector<vector<bool> > visited(n, vector<bool>(m, false));
    const int dr[8] = {-1,-1,-1,0,0,1,1,1};
    const int dc[8] = {-1,0,1,-1,1,-1,0,1};
    int answer = 0;

    for (int r = 0; r < n; ++r) {
        for (int c = 0; c < m; ++c) {
            if (visited[r][c]) continue;
            int value = board[r][c];
            queue<pair<int,int> > q;
            q.push({r,c});
            visited[r][c] = true;
            int cnt = 0;
            int minR = r, maxR = r, minC = c, maxC = c;

            while (!q.empty()) {
                auto [cr,cc] = q.front(); 
                q.pop();
                ++cnt;
                minR = min(minR, cr);
                maxR = max(maxR, cr);
                minC = min(minC, cc);
                maxC = max(maxC, cc);
                for (int k = 0; k < 8; ++k) {
                    int nr = cr + dr[k], nc = cc + dc[k];
                    if (nr < 0 || nr >= n || nc < 0 || nc >= m) 
                        continue;
                    if (visited[nr][nc] || board[nr][nc] != value) 
                        continue;
                    visited[nr][nc] = true;
                    q.push({nr,nc});
                }
            }
            int h = maxR - minR + 1;
            int w = maxC - minC + 1;
            if (h >= 2 && h == w && cnt == h * w) ++answer;
        }
    }
    return answer;
}
