# agentic-template

Bo khung "agentic coding" duoc rut ra tu mot du an monorepo thuc te (domain
goc la bao hiem). Domain cua ban se la CHUNG KHOAN (CTCK) - phan domain da
duoc thay bang placeholder rong (CLAUDE.md muc "Domain Model" va
.claude/rules/domain-model.md) de ban tu dien theo schema/nghiep vu that,
khong bi anh huong boi domain bao hiem cua repo goc.

## Da copy gi, bo gi

Du an goc co ~20 sub-agent, ~60 rules, ~70 skills, ~35 hooks - phan lon gan
chat vao stack cu the (AWS/Pulumi, Statsig, Linear, WunderGraph Cosmo,
Hasura/dbmate, Phoenix SDK, domain bao hiem...). Template nay giu lai CO CHE
(structure + hook mechanics da tu generic) va bo NOI DUNG gan voi stack/domain
do. Bang duoi la inventory day du.

### .claude/rules/ (13 file - luon load vao context)

| File | Noi dung |
|---|---|
| working-style.md | Nguyen tac lam viec: think first, simplicity first, surgical changes, risk assessment truoc hanh dong kho dao nguoc |
| tdd.md | Bat buoc RED - GREEN - REFACTOR |
| no-fallbacks.md | Cam fallback/degrade am tham - fail fast, fail loud |
| no-silent-fallbacks.md | Cam gia tri mac dinh che giau du lieu thieu |
| git-workflow.md | Worktree bat buoc, draft-PR-by-default, serial worktree/PR policy |
| worktree-edit-guard.md | Giai thich 2 invariant cua hook cung ten + limitation da biet |
| backward-compatibility.md | Placeholder - xoa neu project chua co external consumer |
| env-secrets.md | .env luon generated, khong commit - placeholder cho ban dien secret store that |
| use-lsp.md | Uu tien LSP thay vi grep khi dieu huong code |
| generate-random.md | Luon generate UUID/secret that, khong tu bia chuoi |
| claude-code-conventions.md | Quy tac chon rule vs skill vs hook vs agent vs memory |
| testing-checklist.md | Checklist truoc khi coi 1 task la "done" |
| pr-quality-agents.md | Huong dan mo rong: cach them review-agent theo domain sau nay |
| domain-model.md | Placeholder rong danh cho domain chung khoan (CTCK): entity chain, quy uoc, cho doc schema that |
| linear.md | Luong Linear qua MCP (khong dung script rieng) - session-link 1 file, hook chi nudge, model tu goi MCP tool |

### .claude/skills/ (6 skill - load theo nhu cau)

| Skill | Noi dung |
|---|---|
| tdd/SKILL.md | Quy trinh TDD chi tiet + cho dien test runner/convention that |
| git-workflow/SKILL.md | Quy trinh git chi tiet: EnterWorktree - code - commit (5 buoc) - rebase - PR - merge - ExitWorktree |
| claude-code-conventions/SKILL.md | Cach tao rule/skill/hook/agent/memory moi, dung format |
| generate/SKILL.md | Lenh cu the generate UUID/password/hex |
| new-agent/SKILL.md | Cach scaffold 1 sub-agent moi |
| linear-workflow/SKILL.md | Link/unlink session voi Linear issue va cap nhat qua MCP tool truc tiep |

### .claude/agents/ (2 agent mau)

| Agent | Vai tro |
|---|---|
| coder.md | Implementer mac dinh: doc - RED - GREEN - typecheck - test - commit - self-review - digest. KHONG push/tao PR/dung issue tracker |
| reviewer.md | Review diff theo .claude/rules/*.md, chi bao cao, khong sua code |

### .claude/hooks/ (21 hook, da wired san trong settings.json)

| Hook | Su kien | Vai tro |
|---|---|---|
| claude-session-start.sh | SessionStart | Ghi session_id, tu adopt worktree neu session resume vao 1 worktree chua duoc track |
| worktree-guard.sh | UserPromptSubmit | Canh bao neu thu muc hien tai da bi xoa (worktree bi remove) |
| worktree-edit-guard.sh | PreToolUse Edit/Write/MultiEdit/NotebookEdit | Chan edit lac sang worktree khac cung repo, va edit code khi dang o primary+main |
| worktree-post-enter.sh | PostToolUse EnterWorktree | Tu doi ten branch worktree-feat-x thanh feat/x |
| serial-worktree-guard/track/clear.sh | PreToolUse/PostToolUse EnterWorktree/ExitWorktree | Nudge 1 session = 1 worktree tai 1 thoi diem |
| serial-pr-guard.sh | PreToolUse gh pr create | Nudge 1 session = 1 PR mo tai 1 thoi diem |
| pr-draft-default.sh | PreToolUse gh pr create | Bat buoc --draft, tru khi co override tuong minh |
| pr-ready-confirm.sh | PreToolUse gh pr ready | Bat buoc hoi nguoi dung truoc khi go Draft badge |
| command-guard.sh | PreToolUse Bash | Chan git add -A, --no-verify, git worktree add/remove tho |
| tdd-enforce.sh | PreToolUse git commit | Chan commit neu file source moi thieu file test |
| no-fallbacks-guard.sh | PreToolUse Edit/Write | Quet heuristic pattern fallback/degrade trong code moi |
| post-merge-mark-exit.sh + permission-allow-exit-after-merge.sh | PostToolUse Bash + PermissionRequest ExitWorktree | Sau khi gh pr merge thanh cong, tu dong approve ExitWorktree trong 10 phut |
| post-exit-pull-main.sh | PostToolUse ExitWorktree | Fast-forward main o primary checkout sau khi thoat worktree |
| pr-created-agents.sh | PostToolUse Bash | Nhac self-review sau khi tao PR |
| stop-dev-services.sh | SessionEnd | Stub rong - dien khi project co dev-server convention that |
| linear-session-start.sh | SessionStart | Neu session da link Linear issue, nhac model goi get_issue + list_comments qua MCP |
| linear-plan-nudge.sh | PostToolUse ExitPlanMode | Neu da link, nhac model post plan vua duyet thanh comment qua MCP |
| linear-pr-nudge.sh | PostToolUse Bash (gh pr create/ready/merge) | Neu da link, nhac model comment/chuyen state qua MCP |

### .claude/memory/MEMORY.md

Index rong, co san huong dan format (frontmatter name/description/metadata.type)
va 4 loai memory (user, feedback, project, reference) - y het co che memory
ca nhan cua Claude Code nhung o cap TEAM, commit vao git.

### Da CHU DONG bo (khong copy)

AWS/Pulumi/infra-safety, Statsig, Linear, WunderGraph Cosmo/GraphQL-first,
Hasura/dbmate migration-safety, multi-env-companies, i18n 4-locale,
Phoenix SDK release, Oracle second-opinion consult, apple/host/legacy
endpoint police, dev-mode (prod/local/test theo AWS IAM), logging-enforcement
theo logger noi bo, performance-guard theo Kysely, refdata S3,
seed-maintenance, doltgres, per-env-image-tags, dev-session recorder,
codex-coder... - toan bo deu la co che DUNG nhung noi dung 100% gan voi stack
cu the cua du an goc. Xem skill claude-code-conventions de biet cach them lai
mot rule/hook moi theo dung pattern khi project cua ban can.

## Cach dung - bat dau tu dau

### 1. Bien thu muc nay thanh project that cua ban

Chay trong thu muc nay:

    git init
    git add CLAUDE.md README.md .gitignore .claude
    git commit -m "chore: bootstrap from agentic-template scaffold"

Neu ban dinh dung ten khac cho project, doi ten thu muc truoc khi git init,
hoac copy toan bo noi dung (tru .git neu co) sang project da ton tai.

### 2. Dien CLAUDE.md truoc tien

Day la file quan trong nhat - moi rule/skill khac deu gia dinh CLAUDE.md da
mo ta dung tech stack, folder structure, va onboard script. Thu tu nen dien:

1. Project Context - 1 doan mo ta du an la gi.
2. Tech Stack - liet ke that, dung doan.
3. Folder Structure - cap nhat moi khi them 1 sub-app/service lon.
4. Onboard - chi dien khi ban thuc su co scripts/onboard.sh; dung bia.

### 3. Xoa cac placeholder khong ap dung

- Khong co external consumer (SDK doi tac, API public)? Xoa
  .claude/rules/backward-compatibility.md va section tuong ung trong CLAUDE.md.
- Khong co UI/brand? Xoa .claude/soul.md va section Soul and Voice.
- Doi env-secrets.md theo secret store ban that su dung (AWS SSM, GCP Secret
  Manager, Doppler, 1Password, ...).

### 4. Tuy bien cac hook co ghi chu CUSTOMIZE

Ba hook can sua theo stack that truoc khi tin tuong chung 100%:

- .claude/hooks/tdd-enforce.sh - hien chi hieu quy uoc TypeScript
  (sibling .test.ts). Doi sang convention ngon ngu ban dung.
- .claude/hooks/command-guard.sh - DA BAT san enforcement bun/bunx (chan
  npm/npx/node). Neu doi runtime, sua lai block nay.
- .claude/hooks/stop-dev-services.sh - stub rong, dien khi co dev-server.

### 5. Thu nghiem co che truoc khi tin dung

Xem toan bo hook da wire dung chua:

    cat .claude/settings.json

Test 1 hook doc lap, dung file JSON tam thay vi echo inline (tranh loi
quoting tren Windows Git Bash):

    printf "%s" "{\"tool_input\":{\"command\":\"git add -A\"}}" > /tmp/t1.json
    bash .claude/hooks/command-guard.sh < /tmp/t1.json

Ket qua mong doi: in ra ERROR va thoat voi ma loi khac 0.

Mo Claude Code trong thu muc nay va thu EnterWorktree voi ten feat-hello,
se thay branch tu doi thanh feat/hello nho worktree-post-enter.sh.

### 6. Biet truoc 1 gioi han cua worktree-edit-guard.sh

Hook nay chan MOI edit khi ban dang o primary checkout va branch main, ke ca
khi file do thuoc mot project khac hoan toan - no khong kiem tra git-root
cua chinh file dang ghi trong nhanh check primary-on-main. Neu gap tinh
huong nay, dung Bash (cat voi heredoc) thay vi Edit/Write, hoac mo worktree
truoc. Chi tiet trong .claude/rules/worktree-edit-guard.md.

### 7. Bo sung dan theo nhu cau that

Dung them rule/hook/skill cho thu chua ton tai. Khi project bat dau co:

- Issue tracker (Linear/Jira/GitHub Issues) - viet .claude/rules/issue-tracker.md
  moi, theo pattern cua skill claude-code-conventions.
- Cloud infra (Pulumi/Terraform) - viet .claude/rules/infra-safety.md voi
  nguyen tac preview truoc apply.
- i18n nhieu ngon ngu - viet rule va co the them sub-agent i18n.
- PR review theo domain cu the - xem .claude/rules/pr-quality-agents.md.

Moi rule/skill moi nen co Load this rule when va Skip when ro rang.

## Co che hoat dong (tom tat)

- .claude/rules la noi luon duoc nap vao context moi session. Giu ngan.
- .claude/skills chi nap khi can, theo mo ta khop voi viec dang lam.
- .claude/hooks thuc thi quyet dinh mot cach xac dinh, khong phu thuoc model
  co nho rule hay khong.
- .claude/agents la don vi cong viec co the dispatch ra ngoai context chinh.
- .claude/memory la su that ben vung theo thoi gian.
