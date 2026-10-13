# TasQ Network (TasQ) on Robinhood Chain: risk is LOW, with one caveat

`0xdc453b1405cfe25e2afba8e7f4272b0a00437777` · chain 4663 · depth: deep · checks: rug, contract, deployer, holders, honeypot, lp

**At a glance:** Rug risk LOW (0/12) · source verified · owner renounced · deployer has 1 launch, 0 rugged · largest holder is the creator at 11.7% · honeypot SELLABLE (5 of 5 sell simulations passed) · LP LOCKED (99.9999% burned)

**Caveat:** The 112.6M TasQ (11.26% of supply) in the Sablier "lock" can be cancelled at any time. Both streams have sender = recipient = the creator wallet, and `isCancelable = true`. The creator can take them back whenever they want, so this report counts them as creator-held, not locked.

## 1. Rug Scan: LOW (score 0), `RUG_SCAN_OK`
| Signal | Fired? |
|---|---|
| Unverified source | no. Verified FlapTaxTokenV3, solc 0.8.26 |
| Mint authority | no. `_mint` only runs once in `initialize` (fixed 1B supply) |
| Blacklist / pause / fee setters / trading toggle | none in the source |
| Owner not renounced | no. `owner() = 0x0` |
| Proxy / upgradeable | no. EIP-1167 minimal clone (immutable); EIP-1967 slot is 0 |
| Top-1 > 30% / top-10 > 70% | no. 11.7% / 24.2% |
| LP held by deployer | no. 99.9999% of LP is at `0x…dEaD` |

## 2. Contract Audit: `AUDIT_OK`
- The token is an EIP-1167 clone of `0x7777c874…3333`. Today's `sc-audit` run reviewed that implementation and confirmed 0 of 8 candidate findings.
- Clone settings: buy tax 2%, sell tax 2%, both fixed (no setter).
  - The tax only switches off on 2126-09-13, so in practice it is permanent.
  - The anti-farmer phase ends 2026-11-06. After that the tax applies only to the main pool (it currently applies to every registered pool).
- The only owner functions are `startMigration` / `finalizeMigration`. With ownership renounced they can't be called. The state is 2 (TaxEnforcedAntiFarmer), meaning the token has already migrated to the DEX.
- Protocol addresses:
  - Tax processor `0x4e08…5bed`: a clone owned by the Flap portal `0x2660…eb09`, which is a TransparentUpgradeableProxy (an upgradeable proxy).
  - `marketAddress` is the creator, so the creator receives the marketing share of the tax in ETH.
  - Trust note: the portal and tax processor sit at the platform level. Neither can change the token's own logic.
- No live mint, blacklist, drain or upgrade power exists.

## 3. Deployer Trace: `DEPLOYER_TRACE_OK`
- Creator: `0x3d9cf9a0…4f77`. First tx was 2026-10-05; the token launched 2026-10-07 via `newTokenV6` on the Flap portal.
- **1 deployment** (one contract is not a serial pattern).
- Funding: 0.2 ETH from `0xada5…f7cb`, a very high-volume relayer/solver wallet (nonce ~1.4M, mostly `permit2TransferAndMulticall`). This doesn't link the creator to any other launcher.
- What the creator has done since launch:
  - Dev buy of 97.47M (9.7%) at creation, moved within 5 minutes into a Sablier linear stream to themselves (stream #524, 1 month, ends 2026-11-07).
  - Bought a further 29.1M from the pool across 53 buys, paid for with the tax revenue.
  - Burned 8.97M.
  - Added 15.15M to a second stream today (#547, 3 months, ends 2027-01-13).
  - Sent 2M to `0xe4a8…9ab4`.
  - Holds 3M now.
  - **Has made zero sells into the pool.**

## 4. Holder Concentration: HEALTHY, `HOLDER_CONC_OK`
- Holder data is rebuilt from all 44,908 Transfer logs, because `tokenholderlist` is a paid (Pro) Etherscan endpoint. That lowers confidence a little. As a cross-check, the rebuilt pool balance of 66,190,176 exactly matches the pool's onchain reserve.
- 1,168 holders. Burned: 8.97M. Circulating supply: 991.03M.
- Address tags:
  - LP: the pool, 6.62%.
  - Burn: `0xdead`.
  - Sablier: counted as creator-held (the streams are cancelable).
  - Token contract: 208.6K of unsold tax.
  - EIP-7702-delegated wallets: counted as regular wallets (EOAs).

| Measure | Raw | Wallets only (creator + Sablier merged) |
|---|---|---|
| Top 1 | 11.36% | 11.67% (the creator) |
| Top 5 | 23.6% | 18.6% |
| Top 10 | 29.5% | 24.2% |
| Top 50 | 57.0% | 51.1% |
| HHI (concentration index; >2500 = concentrated) | 220 | 182 |
| Holders needed to reach 50% | 37 | 48 |

- Whale clusters: no transfers between the top 30 wallets.
  - 4 of them got their first tokens through RelayRouterV3 (a bridge router, not a cluster signal).
  - 1 wallet, `0x3333…5d10`, fed 2 top-30 wallets. That's a weak link.
  - The other 21 bought on the bonding curve (11) or from the pool (10).

## 5. Honeypot Check: SELLABLE, `HONEYPOT_OK`
- Simulated `transfer(pool, ½ balance)` with `eth_call` (no real transaction) from 5 holders: 2 recent wallets and the top wallets #3, #5 and #7. All 5 returned `true`. Ordinary wallet-to-wallet transfers also succeed.
- Real trading in the last 24 hours: 1,322 sells from 340 different wallets, and 3,758 buys.
- SELLABLE doesn't mean tax-free: the 2% sell tax still applies.

## 6. LP Lock: LOCKED, `LPLOCK_OK`
- Pool: Uniswap V2 pair [`0x1668…be7e`](https://robin.etherscan.io/address/0x16684607c92e1a59302763400cc1641c8f9dbe7e), TasQ/WETH. Factory `0x8bce…937f` (UniswapV2Factory).
- 99.9999% of LP tokens sit at `0x…dEaD`. The remainder is the standard 1000-wei minimum liquidity at `0x0`.
- Reserves: 18.53 WETH / 66.19M TasQ.

**What could still go wrong (heuristic signals, not advice):**
- The creator can cancel the Sablier streams and get 11.3% of supply back right away. Watch for a `CancelLockupStream` on streams 524 and 547.
- The tax is permanent and pays ETH to the creator wallet.

**Notification:** none sent. No multi-check alert trigger fired (rug LOW, no live powers, LP locked, sellable, distribution healthy). Under the "notify only on signal" rule, a clean result sends nothing.

Token: https://robin.etherscan.io/token/0xdc453b1405cfe25e2afba8e7f4272b0a00437777

```
### investigation-report
- Subject: 0xdc453b1405cfe25e2afba8e7f4272b0a00437777 (TasQ Network / TasQ, Robinhood chainid 4663) | checks: rug,contract,deployer,holders,honeypot,lp | depth: deep
- rug: LOW (0/12) — unverified=no, mint=no (init-only), blacklist=no, fees-mutable=no (2%/2% fixed), owner-renounced=yes, proxy=no (EIP-1167 clone), top1=11.7% (deployer-controlled)
- contract: OK — verified=yes, FlapTaxTokenV3 clone of 0x7777…3333 (sc-audit 2026-10-13: 0 confirmed), owner=0x0, state=TaxEnforcedAntiFarmer, taxExpiry=2126-09-13, antiFarmer ends 2026-11-06; taxProcessor 0x4e08…5bed (clone, owner=Flap portal TUP 0x2660…eb09), marketAddress=deployer
- deployer: OK — 0x3d9c…4f77 | 1 deploy (newTokenV6 via Flap portal) | rugged 0 | fresh wallet (2026-10-05) funded 0.2 ETH by high-volume relayer 0xada5…f7cb | 0 sells to pool, 53 buybacks (29.1M), 8.97M burned
- holders: HEALTHY — HHI 182 (raw 220) | holders 1168 | top1 entity 11.67% (deployer+cancelable Sablier) | top10 EOA 24.2% | 50%-in 48 | LP 6.62% (locked), burn 0.90% | no top-30 inter-transfers; weak link 0x3333…5d10→2 wallets
- honeypot: SELLABLE — 5/5 simulated sells to pool returned true (2 recent + top #3/#5/#7); 340 unique real sellers last 24h; 2% sell tax
- lp: LOCKED — pool 0x1668…be7e (UniV2 TasQ/WETH, 18.53 WETH) | locked 99.9999% (0xdead)
- Caveat: Sablier streams #524 (97.47M, ends 2026-11-07) and #547 (15.15M, ends 2027-01-13) are CANCELABLE with sender=recipient=deployer → 11.3% supply is deployer-reclaimable, not locked
- Sources: etherscan=ok (key), tokenholderlist=Pro-only → holders reconstructed from 44,908 Transfer logs via Etherscan getLogs (cross-checked vs pool reserve), rpc=ok (public RPC 429/Cloudflare on bulk getLogs; point reads ok)
- End-state: REPORT_OK (no notify)
```

## Summary
- Ran all six checks at deep depth on chain 4663: Etherscan v2 with the API key, plus the public Robinhood RPC. For bulk log fetches the RPC rate-limited (429) and then served a Cloudflare challenge, so I pulled the logs through Etherscan's getLogs instead.
- Result: `REPORT_OK`. All six sections compiled and none came back unavailable. No notification sent. The only real caveat is the cancelable Sablier "lock" (11.3% of supply the creator can reclaim).
- Files written: only scratch files in `output/` (`inv-src.json`, `inv-logs.json`, `inv-top50.json`). Nothing outside `memory/` and `output/` was changed. The memory log entry is the block above; the workflow appends it.
- Follow-up: re-run near 2026-11-06 (end of the anti-farmer phase) and 2026-11-07 (end of stream #524), or if streams 524 or 547 get cancelled.
