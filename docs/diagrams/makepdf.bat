@ECHO ON

for %%f in ("*\~") do (
    del "%ff"
)

for %%f in (*.dia) do (
    dia --verbose -e "pdf\%%~nf.pdf" -t pdf "%%f" >> makepdflog.log
)
