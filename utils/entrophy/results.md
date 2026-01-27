# Resultados de Entropía

## Entropía de Shannon

| Dominio | Entropía |
|---------|----------|
| google | 1.918296 |
| microsoft | 2.947703 |
| uvg | 1.584963 |
| uspsxcjmvb | 3.121928 |
| uspsn-tn-track | 3.235926 |

## Entropía Relativa / Divergencia KL

| Dominio | Divergencia KL |
|---------|----------------|
| google | 2.104644 |
| microsoft | 1.381477 |
| uvg | 3.737898 |
| uspsxcjmvb | 2.224930 |
| uspsn-tn-track | 1.404527 |

## Interpretación

- **Shannon**: Mayor entropía indica mayor aleatoriedad/complejidad en la distribución de caracteres. `uspsn-tn-track` y `uspsxcjmvb` tienen la mayor entropía.
- **KL Divergence**: Valores más bajos indican que la distribución del texto es más cercana a la distribución de referencia de dominios típicos. `microsoft` y `uspsn-tn-track` son los más "normales", mientras que `uvg` (muy corto) tiene la mayor divergencia.
