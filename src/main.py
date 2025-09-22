# src/main.py
from binance_exchange import BinanceExchange
from bitget_exchange import BitgetExchange

def print_balances(title, balances):
    if not balances:
        print(f"❌ Aucun solde trouvé pour {title}")
        return

    print(f"\n🔗 {title}:")
    for b in balances:
        print(
            f" - {b['asset']:<6} | {b['total']:.6f} "
            f"(dispo: {b['available']:.6f}, "
            f"frozen: {b['frozen']:.6f}, "
            f"locked: {b['locked']:.6f})"
        )

def main():
    print("🚀 Connexion aux exchanges...")

    # === Bitget ===
    bitget = BitgetExchange()
    balances_bitget = bitget.get_all_balances()
    print_balances("Bitget (Spot + Earn)", balances_bitget)

    # === Binance ===
    binance = BinanceExchange()
    balances_binance = binance.get_all_balances()
    print_balances("Binance (Spot + Earn)", balances_binance)

    # === Vue globale ===
    print("\n📊 Vue d’ensemble (Bitget + Binance):")
    combined = {}
    for b in balances_bitget + balances_binance:
        coin = b["asset"]
        combined.setdefault(coin, 0)
        combined[coin] += b["total"]

    for coin, total in combined.items():
        print(f" - {coin:<6} | {total:.6f}")


if __name__ == "__main__":
    main()
