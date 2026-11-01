# Checklist antes de publicar

## Autoria e conteúdo

- [x] Preencher “Minha contribuição” apenas com atividades realizadas por Henrique.
- [x] Inserir apenas um link público autorizado para o site.
- [ ] Confirmar que o texto reconhece a existência de dois contribuidores.
- [ ] Confirmar que nenhuma métrica, funcionalidade ou resultado foi acrescentado sem evidência.

## Isolamento do repositório privado

- [ ] Executar `git status` no repositório privado e confirmar que não houve alteração.
- [ ] Confirmar que este diretório possui um `.git` novo e nenhum remote configurado.
- [ ] Executar `git log` e confirmar que nenhum histórico privado foi herdado.
- [ ] Revisar a árvore completa e confirmar que `.lovable/`, `.github/workflows/` e arquivos comerciais não entraram.

## Revisão de segurança

- [ ] Revisar o diff completo: `git diff --no-index /dev/null <arquivo>` para arquivos ainda não commitados, ou ferramenta equivalente.
- [ ] Procurar chaves, tokens, secrets, JWTs, URLs, e-mails e identificadores de projeto.
- [ ] Confirmar que `.env` está ignorado e que `.env.example` não contém valores.
- [ ] Confirmar que não existem URLs ou referências da infraestrutura de produção.
- [ ] Confirmar que não existem webhooks, pagamentos, preços, produtos ou regras de acesso.
- [ ] Confirmar que não existem migrações, políticas RLS, funções de banco ou templates de e-mail.
- [ ] Confirmar que nenhum CSV, ZIP, questão real ou lote de produção foi incluído.

## Qualidade

- [ ] Rodar `python -m compileall pipeline/scripts`.
- [ ] Rodar o pipeline com uma amostra permitida dos microdados.
- [ ] Conferir os itens enviados para `review`.
- [ ] Revisar o Mermaid no preview do GitHub.
- [ ] Só então criar manualmente o repositório público e configurar o remote.

