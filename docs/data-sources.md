# ICARUS Data Source Catalog

**19 loaded | 1 pipeline ready | 65+ not yet built**
Last updated: 2026-02-25

---

## 1. LOADED (19 sources)

All sources below have working ETL pipelines in `etl/src/icarus_etl/pipelines/` and are loaded into production Neo4j.

| # | Source | URL | Format | Nodes Created | Rels Created | Volume |
|---|--------|-----|--------|---------------|--------------|--------|
| 1 | CNPJ (Receita Federal) | dadosabertos.rfb.gov.br | Bulk CSV (37 ZIPs) | 53.6M Company, 1.98M Person | 24.6M SOCIO_DE | ~85GB uncompressed |
| 2 | TSE (Elections) | dadosabertos.tse.jus.br | Bulk CSV | 2.38M Person, 16.7K Election | 8.2M DOOU, 2.93M CANDIDATO_EM | 2002-2024, 28.7M donations |
| 3 | Transparencia (Contracts) | portaldatransparencia.gov.br | Bulk CSV | 38K Contract, 27.6K Amendment | 32K VENCEU, 29K AUTOR_EMENDA | Federal contracts |
| 4 | CEIS/CNEP (Sanctions) | portaldatransparencia.gov.br | CSV/API | 23.8K Sanction | 23.8K SANCIONADA | Banned companies/persons |
| 5 | BNDES (Dev. Bank Loans) | dadosabertos.bndes.gov.br | CSV | 9.2K Finance | 8.7K RECEBEU_EMPRESTIMO | All public loan operations |
| 6 | PGFN (Tax Debt) | dados.pgfn.fazenda.gov.br | Bulk CSV | 24M Finance | 24M DEVE | Divida ativa da Uniao |
| 7 | ComprasNet/PNCP | compras.dados.gov.br | CSV/API | 1.08M Contract | 1.07M VENCEU | Federal procurement |
| 8 | TCU (Audit Sanctions) | portal.tcu.gov.br/dados-abertos | CSV | 45K Sanction | 45K SANCIONADA | Inabilitados/inidoneos |
| 9 | TransfereGov | plataforma.transferegov.sistema.gov.br | CSV | 71K Amendment, 67K Convenio | 320K BENEFICIOU, 70K GEROU_CONVENIO | Federal transfers |
| 10 | RAIS (Labor Stats) | dados.gov.br | CSV | 29.5K LaborStats | -- | Aggregate by CNAE+UF (no CPF) |
| 11 | INEP (Education) | dados.gov.br | CSV | 224K Education | 18K MANTEDORA_DE | Education census |
| 12 | DATASUS/CNES | cnes.datasus.gov.br | API (Open Data) | 602K Health | 435K OPERA_UNIDADE | Health facility registry |
| 13 | IBAMA (Embargoes) | servicos.ibama.gov.br | API | 79K Embargo | 79K EMBARGADA | Environmental enforcement |
| 14 | Camara (Expenses) | dadosabertos.camara.leg.br | CSV | 4.6M Expense | 4.6M GASTOU, 4.9M FORNECEU | Deputy CEAP expenses |
| 15 | Senado (Expenses) | www12.senado.leg.br/transparencia | CSV | 272K Expense | 272K FORNECEU | Senator CEAPS expenses |
| 16 | ICIJ (Offshore Leaks) | offshoreleaks.icij.org | Bulk CSV | 4.8K OffshoreEntity, 6.6K OffshoreOfficer | 2.3K OFFICER_OF | Panama/Paradise/Pandora papers |
| 17 | OpenSanctions (Global PEPs) | opensanctions.org | Bulk JSON | 118K GlobalPEP | 7.6K GLOBAL_PEP_MATCH | Name-matched to Brazilian entities |
| 18 | CVM (Proceedings) | dados.cvm.gov.br | CSV (ZIP) | 522 CVMProceeding | 1.1K CVM_SANCIONADA | Securities sanctions |
| 19 | Servidores (Public Servants) | portaldatransparencia.gov.br | Bulk CSV | 635K PublicOffice, 632K Person | 636K RECEBEU_SALARIO, 36K SAME_AS | Federal servants + salaries |

**Production totals:** 96.8M nodes, 71.4M relationships across 20 node labels and 20+ relationship types.

---

## 2. PIPELINE READY (1 source)

| Source | Pipeline | Status | Workaround |
|--------|----------|--------|------------|
| DOU (Diario Oficial da Uniao) | `etl/src/icarus_etl/pipelines/dou.py` | Blocked: Querido Diario API returns Cloudflare challenge pages | Use official Imprensa Nacional XML dumps at `in.gov.br/acesso-a-informacao/dados-abertos/base-de-dados`. Alternative: Scrapling library for stealth browser fetching. |

---

## 3. NOT BUILT (65+ sources)

### 3.1 CGU / Transparencia Portal (8 sources)

| # | Source | URL | Format | Est. Volume | Nodes/Rels | Value | Notes |
|---|--------|-----|--------|-------------|------------|-------|-------|
| 1 | CGU PEP List | portaldatransparencia.gov.br/download-de-dados/pep | CSV | ~100K | Person(pep=true) | HIGH | Replaces hardcoded PEP_ROLES frozenset |
| 2 | CEAF (Expelled Servants) | portaldatransparencia.gov.br/download-de-dados/ceaf | CSV + API | ~10K | Expulsion nodes | HIGH | Fired for misconduct |
| 3 | CEPIM (Barred NGOs) | portaldatransparencia.gov.br/download-de-dados/cepim | CSV | ~5K | BarredNGO nodes | MEDIUM | NGOs barred from new agreements |
| 4 | Acordos de Leniencia | portaldatransparencia.gov.br/download-de-dados/acordos-leniencia | CSV | ~34 records | LeniencyAgreement nodes | VERY HIGH | Companies that confessed wrongdoing |
| 5 | CPGF (Govt Credit Cards) | portaldatransparencia.gov.br/download-de-dados/cpgf | Bulk CSV | Millions/yr | GovCardExpense nodes | HIGH | Corporate credit card spending |
| 6 | Viagens a Servico | portaldatransparencia.gov.br/download-de-dados/viagens | CSV | ~500K/yr | GovTravel nodes | MEDIUM | Government travel expenses |
| 7 | Bolsa Familia/BPC | portaldatransparencia.gov.br/download-de-dados/bolsa-familia-pagamentos | CSV | ~20M | SocialBenefit nodes | LOW | CPFs masked by LGPD |
| 8 | Renuncias Fiscais | portaldatransparencia.gov.br/download-de-dados/renuncias | CSV | Millions | TaxWaiver nodes | HIGH | R$414B+ in tax waivers |

### 3.2 BCB / Central Bank (5 sources)

| # | Source | URL | Format | Est. Volume | Nodes/Rels | Value | Notes |
|---|--------|-----|--------|-------------|------------|-------|-------|
| 9 | BCB Penalidades | dados.bcb.gov.br | CSV | ~10K | BankPenalty nodes | HIGH | Fines on financial institutions |
| 10 | BCB Multas | dados.bcb.gov.br | CSV | ~5K | BankFine nodes | HIGH | Administrative fines |
| 11 | ESTBAN | dados.bcb.gov.br | CSV | ~500K/mo | BankingStats nodes | LOW | Bank branch balance sheets |
| 12 | IF.data | dados.bcb.gov.br | CSV | ~2K quarterly | FinancialInstitution nodes | LOW | Financial institution metrics |
| 13 | BCB Liquidacao | dados.bcb.gov.br | CSV | ~200 | BankLiquidation nodes | MEDIUM | Liquidated financial institutions |

### 3.3 Judiciary (5 sources)

| # | Source | URL | Format | Est. Volume | Nodes/Rels | Value | Notes |
|---|--------|-----|--------|-------------|------------|-------|-------|
| 14 | CNJ DataJud | api-publica.datajud.cnj.jus.br | REST API (self-service key) | Tens of millions | LegalCase nodes | VERY HIGH | Proceedings across all courts |
| 15 | STJ Dados Abertos | dadosabertos.stj.jus.br | CSV/XML | ~500K | LegalCase nodes | HIGH | Superior court decisions |
| 16 | CNCIAI (Improbidade) | cnj.jus.br (part of DataJud) | API | ~10K | ImprobityCase nodes | VERY HIGH | Administrative misconduct convictions |
| 17 | CARF (Tax Appeals) | carf.fazenda.gov.br | Structured | ~500K | TaxAppeal nodes | MEDIUM | Federal tax appeal decisions |
| 18 | STF via BigQuery | basedosdados.org (br_stf_corte_aberta) | BigQuery | ~100K | SupremeCourtCase nodes | MEDIUM | Supreme court votes |

### 3.4 Regulatory Agencies (11 sources)

| # | Source | URL | Format | Est. Volume | Nodes/Rels | Value | Notes |
|---|--------|-----|--------|-------------|------------|-------|-------|
| 19 | ANP (Oil/Gas Royalties) | dados.gov.br/dados/conjuntos-dados/anp | API + CSV | ~100K/yr | Royalty, FuelPrice nodes | MEDIUM | Oil royalties + fuel pricing |
| 20 | ANEEL (Energy) | dadosabertos.aneel.gov.br | API | ~50K | EnergyContract nodes | MEDIUM | Energy concessions and contracts |
| 21 | ANM (Mining) | dados.gov.br/dados/conjuntos-dados/anm | API + CSV | ~100K | MiningConcession nodes | HIGH | Mining rights, often tied to deforestation |
| 22 | ANTT (Roads) | dados.gov.br/dados/conjuntos-dados/antt | API | ~10K | TransportContract nodes | LOW | Transport concessions |
| 23 | ANS (Health Insurance) | dados.gov.br/dados/conjuntos-dados/ans | API | ~50K | HealthPlan nodes | LOW | Health plan operators |
| 24 | ANVISA (Drug/Food) | dados.gov.br/dados/conjuntos-dados/anvisa | API | ~100K | RegulatoryApproval nodes | LOW | Product registrations |
| 25 | ANAC (Aviation) | dados.gov.br/dados/conjuntos-dados/anac | API | ~10K | AviationConcession nodes | LOW | Airport concessions |
| 26 | ANTAQ (Waterways) | dados.gov.br/dados/conjuntos-dados/antaq | API | ~5K | PortContract nodes | LOW | Port authority contracts |
| 27 | ANA (Water) | dados.gov.br/dados/conjuntos-dados/ana | API | ~10K | WaterConcession nodes | LOW | Water resource grants |
| 28 | ANATEL (Telecom) | dados.gov.br/dados/conjuntos-dados/anatel | API | ~50K | TelecomLicense nodes | LOW | Telecom licenses |
| 29 | SUSEP (Insurance) | dados.gov.br/dados/conjuntos-dados/susep | CSV | ~10K | InsuranceEntity nodes | LOW | Insurance market data |

### 3.5 Financial / Securities (2 sources)

| # | Source | URL | Format | Est. Volume | Nodes/Rels | Value | Notes |
|---|--------|-----|--------|-------------|------------|-------|-------|
| 30 | CVM Full (Ownership/Funds) | dados.cvm.gov.br | CSV | Millions | DETEM_PARTICIPACAO rels | HIGH | Shareholder chains, fund ownership |
| 31 | Receita DIRBI | dados.gov.br | CSV | Large | TaxBenefit nodes | MEDIUM | Tax benefit declarations |

### 3.6 Environmental (3 sources)

| # | Source | URL | Format | Est. Volume | Nodes/Rels | Value | Notes |
|---|--------|-----|--------|-------------|------------|-------|-------|
| 32 | MapBiomas Alerta | alerta.mapbiomas.org/api | REST API | 465K+ alerts | DeforestationAlert nodes | HIGH | Validated deforestation, property overlap |
| 33 | SiCAR (Rural Registry) | car.gov.br/publico/municipios/downloads | Bulk shapefiles | ~7M properties | RuralProperty nodes | HIGH | Rural property boundaries + owners |
| 34 | ICMBio/CNUC | icmbio.gov.br | API | ~2.5K | ConservationUnit nodes | LOW | Protected area boundaries |

### 3.7 Labor (2 sources)

| # | Source | URL | Format | Est. Volume | Nodes/Rels | Value | Notes |
|---|--------|-----|--------|-------------|------------|-------|-------|
| 35 | CAGED | basedosdados.org (br_me_caged) | BigQuery | ~2M/mo | LaborMovement nodes | MEDIUM | Monthly hiring/firing (no CPF in public data) |
| 36 | RAIS Microdata | basedosdados.org (br_me_rais) | BigQuery | ~50M/yr | DetailedLabor nodes | MEDIUM | Identified data requires formal authorization |

### 3.8 Budget / Fiscal (4 sources)

| # | Source | URL | Format | Est. Volume | Nodes/Rels | Value | Notes |
|---|--------|-----|--------|-------------|------------|-------|-------|
| 37 | SIOP Emendas | siop.planejamento.gov.br | CSV + API | ~30K/yr | DetailedAmendment nodes | HIGH | Parliamentary amendment execution details |
| 38 | SICONFI | siconfi.tesouro.gov.br | REST API (siconfipy) | ~5.5K municipalities | MunicipalFinance nodes | MEDIUM | Municipal/state fiscal data |
| 39 | Tesouro Emendas | tesouro.gov.br | CSV | ~50K | TreasuryAmendment nodes | HIGH | Treasury-tracked amendment spending |
| 40 | SIGA Brasil | www12.senado.leg.br/orcamento/sigabrasil | CSV export | Massive | BudgetExecution nodes | MEDIUM | Full federal budget execution |

### 3.9 Legislative (4 sources)

| # | Source | URL | Format | Est. Volume | Nodes/Rels | Value | Notes |
|---|--------|-----|--------|-------------|------------|-------|-------|
| 41 | Camara Full API (Votes/Bills) | dadosabertos.camara.leg.br/api/v2 | REST API + BigQuery | Millions | Vote, Bill nodes | MEDIUM | Deputy votes, bill authorship |
| 42 | Senado Full API (Votes/CPIs) | legis.senado.leg.br/dadosabertos | REST API + BigQuery | Large | SenateVote, CPI nodes | MEDIUM | Senate votes, CPI details |
| 43 | TSE Filiados | basedosdados.org (br_tse_eleicoes.filiacao_partidaria) | BigQuery | ~15M | PartyMember edges | MEDIUM | Party membership history |
| 44 | TSE Bens (Candidate Assets) | basedosdados.org (br_tse_eleicoes.bens_candidato) | BigQuery | ~500K | DeclaredAsset nodes | HIGH | Declared patrimony per election |

### 3.10 International Sanctions (5 sources)

| # | Source | URL | Format | Est. Volume | Nodes/Rels | Value | Notes |
|---|--------|-----|--------|-------------|------------|-------|-------|
| 45 | OFAC SDN | sanctionssearch.ofac.treas.gov | Direct CSV | ~12K | InternationalSanction nodes | HIGH | US Treasury sanctions list |
| 46 | EU Sanctions | data.europa.eu/data/datasets/consolidated-list-of-persons | Direct CSV | ~5K | InternationalSanction nodes | HIGH | EU consolidated sanctions |
| 47 | UN Sanctions | scsanctions.un.org/resources/xml | Direct XML | ~2K | InternationalSanction nodes | HIGH | UN Security Council sanctions |
| 48 | World Bank Debarment | worldbank.org/en/projects-operations/procurement/debarred-firms | CSV (OpenSanctions mirror) | ~1K | InternationalSanction nodes | MEDIUM | Debarred firms/individuals |
| 49 | INTERPOL Red Notices | interpol.int/How-we-work/Notices/Red-Notices | REST API | ~7K | InternationalNotice nodes | MEDIUM | Requires API key |

### 3.11 State / Municipal (10+ sources)

| # | Source | URL | Format | Est. Volume | Nodes/Rels | Value | Notes |
|---|--------|-----|--------|-------------|------------|-------|-------|
| 50 | PNCP Full | pncp.gov.br/api/consulta | Swagger REST API | Massive | Procurement nodes | HIGH | National procurement portal, paginate by date |
| 51 | TCE-SP | transparencia.tce.sp.gov.br | REST API | Large | StateProcurement nodes | HIGH | Sao Paulo state audit court |
| 52 | TCE-PE | sistemas.tce.pe.gov.br | REST API (CPF/CNPJ search) | Large | StateProcurement nodes | MEDIUM | Pernambuco audit court |
| 53 | TCE-RJ | dados.tce.rj.gov.br | REST API | Large | StateProcurement nodes | MEDIUM | Rio de Janeiro audit court |
| 54 | TCE-RS | portal.tce.rs.gov.br | Bulk downloads | Large | StateProcurement nodes | MEDIUM | Rio Grande do Sul audit court |
| 55 | MiDES | basedosdados.org (br_mides) | BigQuery | Massive | MunicipalProcurement nodes | VERY HIGH | 72% of municipalities covered |
| 56 | Querido Diario | queridodiario.ok.org.br/api | REST API + bulk ZIPs | 104K+ issues | MunicipalGazetteAct nodes | HIGH | Municipal gazette full text |
| 57-66 | State Transparency Portals | (SP, MG, BA, CE, GO, PR, SC, RS, PE, RJ) | Varies | Varies | StateExpense nodes | MEDIUM | Each state has its own portal |

---

## 4. GITHUB SHORTCUTS (pre-processed data)

Community-maintained datasets and tools that accelerate ingestion.

| # | Repo / Source | What | Volume | Value | Status |
|---|---------------|------|--------|-------|--------|
| G1 | brasil-io-public.s3.amazonaws.com (holding.csv.gz) | Company-to-company ownership chains | 787K rels, 9MB | HIGH | Ready to load |
| G2 | SINARC | Pre-built anti-corruption graph | 90GB | REFERENCE | Format unclear, use as validation |
| G3 | cnpj-chat/cnpj-data-pipeline | State-level CNPJ Parquet from GitHub Releases | Large | MEDIUM | Alternative CNPJ format |
| G4 | rictom/rede-cnpj | Pre-computed CNPJ relationship SQLite | Large | MEDIUM | Includes TSE/Transparencia crosslinks |
| G5 | hackfestcc/dados-hackfestcc | Curated anti-corruption datasets | Small | LOW | Reference datasets |
| G6 | DanielFillol/DataJUD_API_CALLER | Go-based DataJud bulk downloader | -- | HIGH | Speeds up CNJ ingestion |
| G7 | Serenata de Amor (suspicions.xz) | Flagged CEAP anomalies | 8K records | MEDIUM | Pre-analyzed deputy expenses |
| G8 | mcp-senado | MCP server wrapping Senate API (56 tools) | -- | LOW | Developer tool, not data |
| G9 | mcp-portal-transparencia | MCP server wrapping Transparency Portal API | -- | LOW | Developer tool, not data |

---

## 5. BIGQUERY DATASETS (via Base dos Dados)

[basedosdados.org](https://basedosdados.org) provides cleaned, standardized Brazilian public data in BigQuery. Free tier has limits; paid plans for heavy use.

| BQ Dataset ID | Key Tables | Loaded? | Notes |
|---------------|------------|---------|-------|
| br_rf_cnpj | empresas, socios, estabelecimentos | YES (direct CSV) | Used direct Receita download instead |
| br_tse_eleicoes | candidatos, receitas, despesas, bens_candidato, filiacao_partidaria | PARTIAL | Candidates + donations loaded via TSE direct; bens + filiados not yet |
| br_me_rais | microdados_vinculos | PARTIAL | Aggregate loaded; microdata requires formal auth |
| br_me_caged | microdados_movimentacao | NO | Monthly labor data |
| br_stf_corte_aberta | decisoes | NO | Supreme court decisions |
| br_camara_dados_abertos | votacao, proposicao, deputado | PARTIAL | Expenses loaded; votes/bills not yet |
| br_senado_cpipedia | cpi | NO | CPI investigation data |
| br_bd_diretorios_brasil | municipio, uf, setor_censitario | NO | Reference tables for joins |
| br_mides | licitacao, contrato, item | NO | Municipal procurement (72% coverage) |

---

## 6. INGESTION PRIORITY MATRIX

Recommended build order based on: value for pattern detection, implementation effort, and data volume.

| Priority | Source | Effort | Volume | Value | Rationale |
|----------|--------|--------|--------|-------|-----------|
| 1 | CGU PEP List | Trivial (CSV) | ~100K | HIGH | Replaces hardcoded PEP_ROLES; authoritative PEP classification |
| 2 | CEAF (Expelled Servants) | Easy (CSV) | ~10K | HIGH | Servants expelled for misconduct; cross-ref with companies |
| 3 | Acordos de Leniencia | Trivial (CSV) | ~34 | VERY HIGH | Companies that admitted wrongdoing; tiny dataset, immense value |
| 4 | OFAC SDN | Easy (CSV) | ~12K | HIGH | International sanctions; direct download, well-structured |
| 5 | Brasil.IO Holdings | Trivial (9MB download) | 787K rels | HIGH | Company-to-company ownership chains; immediate graph enrichment |
| 6 | DOU via IN XML | Medium (XML parsing) | Large | HIGH | Bypasses Cloudflare; official gazette appointments and acts |
| 7 | TSE Bens (Candidate Assets) | Easy (BigQuery) | ~500K | HIGH | Declared patrimony; detect unexplained wealth growth |
| 8 | TSE Filiados (Party Members) | Easy (BigQuery) | ~15M | MEDIUM | Party membership history; useful for political network mapping |
| 9 | CVM Full Ownership | Medium (CSV) | Millions | HIGH | Shareholder chains reveal hidden beneficial ownership |
| 10 | CNJ DataJud | Medium (API + key) | Massive | VERY HIGH | Judicial proceedings; largest gap in current graph |

### Effort Scale
- **Trivial**: Direct CSV download, schema matches existing patterns, <1 day
- **Easy**: CSV/BigQuery, minor transforms needed, 1-2 days
- **Medium**: API pagination, format conversion, or authentication required, 3-5 days
- **Hard**: Scraping, Cloudflare bypass, complex parsing, or formal data request, 1-2 weeks
