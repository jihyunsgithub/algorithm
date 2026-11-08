#include <string>
#include <vector>
#include <unordered_map>
#include <queue>

using namespace std;

int toMinute(const string& s) {
    return stoi(s.substr(0, 2)) * 60 + stoi(s.substr(3, 2));
}

string solution(vector<string> preferences,
                vector<vector<string>> requests) {
    int n = (int)preferences.size();
    unordered_map<string, int> idx;
    for (int i = 0; i < n; ++i) idx[preferences[i]] = i;

    struct Offer { int st, en, from, to; };
    vector<Offer> offers;
    for (const auto& r : requests) {
        //교환 가능한 티켓인지 확인 => 둘 중 하나라도 교환할 수 없는 티켓이면 패스
        if (!idx.count(r[2]) || !idx.count(r[3])) 
            continue;
        // 상대가 원하는 것은 r[3], 상대가 제공하는 것은 r[2]
        // 내가 r[3]을 가지고 있으면 r[2]를 얻는다.

        //티켓 정보를 정수 정보 구조체로 바꿈.
        offers.push_back({toMinute(r[0]), toMinute(r[1]), idx[r[3]], idx[r[2]]});
    }

    vector<bool> reachable(n, false);
    reachable[0] = true;
    //교환을 방향 그래프로 편환 후 bfs로 탐색
    for (int t = 0; t < 24 * 60; ++t) {
        //인접 리스트, e.from으로 바꿀 수 있는 e.to들을 정리
        vector<vector<int>> adj(n);
        for (const auto& e : offers) {
            if (e.st <= t && t <= e.en)
                adj[e.from].push_back(e.to);
        }

        queue<int> q;
        for (int i = 0; i < n; ++i)
            if (reachable[i]) 
                q.push(i);

        // 교환 시간이 0이므로 한 시각에 연쇄 교환 가능
        while (!q.empty()) {
            int cur = q.front(); q.pop();
            for (int nxt : adj[cur]) {
                if (reachable[nxt]) 
                    continue;
                reachable[nxt] = true;
                q.push(nxt);
            }
        }
    }
    //최대 도달 가능한 부스 반환
    for (int i = n - 1; i >= 0; --i)
        if (reachable[i]) return preferences[i];
    return preferences[0];
}
