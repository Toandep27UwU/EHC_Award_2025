#include <stdio.h>
#include <stdlib.h>

typedef long long ll;

typedef struct { ll *a; int n; } Heap;
void hp_init(Heap *h, int cap){ h->a = (ll*)malloc(sizeof(ll)*(cap+5)); h->n = 0; }
void hp_push(Heap *h, ll x){ int i = ++h->n; h->a[i] = x; while (i>1 && h->a[i>>1] < h->a[i]){ ll t=h->a[i]; h->a[i]=h->a[i>>1]; h->a[i>>1]=t; i>>=1; } }
void hp_pop(Heap *h){ h->a[1] = h->a[h->n--]; int i=1; while (1){ int l=i<<1, r=l+1, mx=i; if (l<=h->n && h->a[l]>h->a[mx]) mx=l; if (r<=h->n && h->a[r]>h->a[mx]) mx=r; if (mx==i) break; ll t=h->a[i]; h->a[i]=h->a[mx]; h->a[mx]=t; i=mx; } }
ll hp_top(Heap *h){ return h->n? h->a[1] : 0; }
int hp_empty(Heap *h){ return h->n==0; }

typedef struct Node{ ll p; int next; } Node;

int main(){
    int n,m,t;
    if (scanf("%d %d %d",&n,&m,&t)!=3) return 0;

    int *L = (int*)malloc(sizeof(int)*m);
    int *R = (int*)malloc(sizeof(int)*m);
    ll  *P = (ll*) malloc(sizeof(ll)*m);
    for(int i=0;i<m;i++) scanf("%d %d %lld",&L[i],&R[i],&P[i]);

    if (t>n){ puts("0"); return 0; }

    int T = n - t + 1;

    int valid=0;
    for(int i=0;i<m;i++) if (L[i] <= R[i]-t+1) valid++;

    int *headAdd = (int*)malloc(sizeof(int)*(T+2));
    int *headRem = (int*)malloc(sizeof(int)*(T+2));
    for(int i=0;i<=T+1;i++) headAdd[i]=headRem[i]=-1;

    Node *ADD = (Node*)malloc(sizeof(Node)*valid);
    Node *REM = (Node*)malloc(sizeof(Node)*valid);
    int pa=0, pr=0;

    for(int i=0;i<m;i++){
        int start=L[i], end=R[i]-t+1;
        if (start>end) continue;
        ADD[pa]=(Node){P[i], headAdd[start]}; headAdd[start]=pa++;
        REM[pr]=(Node){P[i], headRem[end+1]}; headRem[end+1]=pr++;
    }

    Heap active, trash; hp_init(&active, valid); hp_init(&trash, valid);

    ll *gain = (ll*)calloc(T+2, sizeof(ll));

    for(int s=1;s<=T;s++){
        for(int it=headAdd[s]; it!=-1; it=ADD[it].next) hp_push(&active, ADD[it].p);
        for(int it=headRem[s]; it!=-1; it=REM[it].next) hp_push(&trash, REM[it].p);
        while(!hp_empty(&active) && !hp_empty(&trash) && hp_top(&active)==hp_top(&trash)){ hp_pop(&active); hp_pop(&trash); }
        gain[s] = hp_empty(&active)? 0 : hp_top(&active);
    }

    ll *dp = (ll*)calloc(n+1, sizeof(ll));
    for(int i=1;i<=n;i++){
        dp[i]=dp[i-1];
        if (i>=t){
            ll cand = dp[i-t] + gain[i-t+1];
            if (cand>dp[i]) dp[i]=cand;
        }
    }
    printf("%lld\n", dp[n]);
    return 0;
}
