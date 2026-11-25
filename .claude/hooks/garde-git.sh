#!/usr/bin/env bash
# Hook PreToolUse (Bash) : empêche Claude de pousser sur main ou de forcer un push.
# Le workflow du projet impose issue → branche → PR relue, et main n'est pas forcément protégée par GitHub
# (seul Chezrush, administrateur du dépôt, peut la protéger). Les règles deny de settings.json interdisent déjà
# git commit et git push à Claude ; ce hook reste une seconde barrière si ces règles sont assouplies.
# Code de sortie 2 = action bloquée, le message sur stderr est renvoyé à Claude.

cmd=$(jq -r '.tool_input.command // ""')

# Rien à vérifier si la commande ne contient pas de git push.
grep -qE '(^|[;&|[:space:]])git[[:space:]]+push([[:space:]]|$)' <<<"$cmd" || exit 0

if grep -qE '[[:space:]](--force|--force-with-lease|-f)([[:space:]=]|$)' <<<"$cmd"; then
  echo "Push forcé interdit par le hook du projet. Si c'est vraiment nécessaire, l'utilisateur le fait lui-même." >&2
  exit 2
fi

branch=$(git -C "${CLAUDE_PROJECT_DIR:-.}" branch --show-current 2>/dev/null)

# Push explicite vers main (git push origin main, HEAD:main, refs/heads/main) ou depuis main.
if grep -qE '([[:space:]]|:)(refs/heads/)?main([[:space:]]|$)' <<<"$cmd" || [ "$branch" = "main" ]; then
  echo "Pas de push sur main : crée une branche, pousse-la et ouvre une PR liée à son issue." >&2
  exit 2
fi

exit 0
