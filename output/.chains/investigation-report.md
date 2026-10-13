ℹ️ Investigation Report — TasQ (Robinhood Chain)

**Investigation Report — TasQ Network (TasQ) · Robinhood Chain · deep · all 6 checks**

**Verdict: REPORT_OK, rug risk LOW (0/12).** Contract is verified and renounced, LP is burned, sells go through. One caveat: 11.3% of supply sits in a Sablier stream the creator can cancel.

| Check | Result |
|---|---|
| Rug | LOW (0/12): verified, owner `0x0`, no mint/blacklist/pause/fee setters, not a proxy (EIP-1167 clone) |
| Contract | AUDIT_OK: FlapTaxTokenV3 clone, fixed 2%/2% tax, no live mint/upgrade/blacklist/drain power |
| Deployer | OK: `0x3d9c…4f77` has 1 launch, 0 rugged, **0 sells into the pool** |
| Holders | HEALTHY: HHI 182, top-1 entity 11.7% (creator + Sablier), top-10 wallets 24.2% *(holder table from this morning's run)* |
| Honeypot | SELLABLE: 5/5 fresh simulated sells returned true, including the creator wallet |
| LP | LOCKED: UniV2 TasQ/WETH, 99.9999% of LP at `0x…dEaD`, creator holds 0 LP |

**What changed since this morning's run:**
- Pool moved from 18.53 WETH / 66.19M TasQ to **16.44 WETH / 74.67M TasQ**, so the price is down about 21%.
- From 09:00 to 16:20 UTC, about 96.9M TasQ was sold into the pool and 89.3M bought out of it. Most of that flow went through router/aggregator contracts. The biggest direct wallet seller was `0x77d1…99c1` with 6.53M. None of it came from the creator.
- The Sablier streams are intact. Custody still holds 112.62M TasQ, with no withdrawals and no cancel.

**Caveats:**
- Streams #524 (97.47M, ends 2026-11-07) and #547 (15.15M, ends 2027-01-13) have sender = recipient = creator and can be cancelled. Treat them as creator-held, not locked.
- The 2% tax is permanent and pays ETH to the creator wallet. The anti-farmer phase ends 2026-11-06.
- These are heuristic risk signals, not advice.

Token: https://robin.etherscan.io/token/0xdc453b1405cfe25e2afba8e7f4272b0a00437777
Pool: https://robin.etherscan.io/address/0x16684607c92e1a59302763400cc1641c8f9dbe7e

🔗 https://robin.etherscan.io/token/0xdc453b1405cfe25e2afba8e7f4272b0a00437777