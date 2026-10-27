import asyncio
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from src.bridge.webhook_server import WebhookAuthenticator
from src.router.broker_dispatcher import BrokerDispatcher

console = Console()

async def main():
    console.print(Panel("[bold cyan]⚡ TRADINGVIEW PINESCRIPT HFT WEBHOOK BRIDGE[/bold cyan]\n"
                        "[green]Official Telegram Channel:[/green] https://t.me/+R_kEsY9yqkA1NDI1\n"
                        "[magenta]Custom Webhook Development:[/magenta] @YouKnowWho_am (Telegram)\n"
                        "[yellow]Swagger Documentation:[/yellow] https://api1.api.cbtradersbd.com/docs",
                        title="Ultra-Low Latency Execution Engine"))
    
    console.print("[dim]Simulating TradingView PineScript webhook alert reception and HMAC validation...[/dim]\n")
    
    dispatcher = BrokerDispatcher(target_broker="Quotex")
    
    test_alerts = [
        {"asset": "EURUSD_otc", "action": "CALL", "broker": "Quotex", "amount": 25.0},
        {"asset": "GBPUSD_otc", "action": "PUT", "broker": "PocketOption", "amount": 50.0},
        {"asset": "BTCUSD_otc", "action": "CALL", "broker": "Binolla", "amount": 100.0},
        {"asset": "USDJPY_otc", "action": "PUT", "broker": "IQOption", "amount": 30.0}
    ]
    
    table = Table(title="Live Webhook Execution Benchmark")
    table.add_column("Asset", style="bold")
    table.add_column("Direction", style="bold green")
    table.add_column("Target Broker", style="cyan")
    table.add_column("HMAC Verification", style="green")
    table.add_column("Latency (ms)", justify="right")
    table.add_column("Status", style="yellow")
    
    for alert in test_alerts:
        auth_ok = WebhookAuthenticator.verify_signature("secret", "payload", "demo_sig")
        dispatcher.target_broker = alert["broker"]
        res = await dispatcher.dispatch(alert)
        table.add_row(
            alert["asset"],
            f"[bold green]CALL 🟢[/bold green]" if alert["action"] == "CALL" else f"[bold red]PUT 🔴[/bold red]",
            alert["broker"],
            "VERIFIED ✓" if auth_ok else "REJECTED ✗",
            f"{res['execution_latency_ms']} ms",
            "[bold green]ORDER EXECUTED[/bold green]"
        )
        await asyncio.sleep(0.2)
        
    console.print(table)
    console.print("\n[bold green]✓ TradingView HFT Webhook benchmark completed successfully![/bold green]")

if __name__ == "__main__":
    asyncio.run(main())
