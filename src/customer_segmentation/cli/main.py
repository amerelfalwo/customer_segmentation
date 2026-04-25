"""
Command-line interface for Customer Segmentation API
"""

import sys
import json
import argparse
from ..client import SegmentationClient, Customer

def print_result(result):
    """Print segmentation result in a nice format"""
    print("\n" + "=" * 60)
    print(f"CLUSTER: {result.cluster}")
    print(f"SEGMENT: {result.segment_name}")
    print(f"CONFIDENCE: {result.confidence_score * 100:.1f}%")
    print("=" * 60)
    print(f"Description: {result.description}")
    print("\nCharacteristics:")
    for key, value in result.characteristics.items():
        print(f"  - {key}: {value:.2f}")
    print("=" * 60 + "\n")

def main():
    parser = argparse.ArgumentParser(description="Customer Segmentation CLI")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Health command
    subparsers.add_parser("health", help="Check API health")

    # Segments command
    subparsers.add_parser("segments", help="Show all segments")

    # Predict command
    predict_parser = subparsers.add_parser("predict", help="Predict segment for a customer")
    predict_parser.add_argument("age", type=float)
    predict_parser.add_argument("income", type=float)
    predict_parser.add_argument("spent", type=float)
    predict_parser.add_argument("web_purchases", type=float)
    predict_parser.add_argument("store_purchases", type=float)
    predict_parser.add_argument("web_visits", type=float)
    predict_parser.add_argument("recency", type=float)

    args = parser.parse_args()

    client = SegmentationClient()

    try:
        if args.command == "health":
            print("\nChecking API health...")
            health = client.health()
            print(json.dumps(health, indent=2))

        elif args.command == "segments":
            print("\nCustomer Segments:")
            segments = client.get_segments()
            for cluster_id, info in segments.items():
                print(f"\n{info['name'].upper()}")
                print(f"  ID: {cluster_id}")
                print(f"  Description: {info['description']}")
                print(f"  Characteristics:")
                for key, value in info['characteristics'].items():
                    print(f"    - {key}: {value:.2f}")

        elif args.command == "predict":
            customer = Customer(
                age=args.age,
                Income=args.income,
                total_spent=args.spent,
                NumWebPurchases=args.web_purchases,
                NumStorePurchases=args.store_purchases,
                NumWebVisitsMonth=args.web_visits,
                Recency=args.recency
            )
            print(f"\nPredicting segment for customer: {customer}")
            result = client.predict(customer)
            print_result(result)
        
        else:
            parser.print_help()

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
