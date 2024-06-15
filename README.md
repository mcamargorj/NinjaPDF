NINJA PDF

Este repositório contém uma aplicação web desenvolvida em Flask para remover restrições de arquivos PDF protegidos por senha, incluindo bloqueios como impressão e cópia de conteúdo.
Funcionalidades

    Upload de Arquivos: Envie arquivos PDF através da interface web.
    Desbloqueio de PDF: Remove senhas e outras restrições de arquivos PDF carregados. O PDF desbloqueado pode ser baixado após o processamento.
    Limpeza e Restauração: Opções para limpar a pasta de uploads e restaurar a aplicação ao estado inicial.

Uso

    Execução:
        Execute o arquivo app.py para iniciar a aplicação Flask.
        Acesse a aplicação através do navegador no endereço http://localhost:5000.

    Como Usar:
        Selecione um arquivo PDF na página inicial e envie-o.
        Forneça a senha, se necessário, para desbloquear o PDF.
        Após o processamento, faça o download do PDF desbloqueado.

    Limpeza da Pasta de Uploads:
        Para remover todos os arquivos enviados, acesse http://localhost:5000/restaurar.

Observações

    Configure o diretório de uploads (uploads) e as permissões corretamente no servidor.
    Este projeto é uma demonstração básica e pode ser expandido com melhorias adicionais.

Licença

Este projeto está sob a licença MIT.
