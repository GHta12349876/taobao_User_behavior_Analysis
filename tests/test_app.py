"""
Test script for the Taobao User Behavior Analysis application.
This script verifies that all modules can be imported and basic functions work correctly.
"""

import sys
import pandas as pd


def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    try:
        import streamlit as st
        print("✓ Streamlit imported")
    except ImportError as e:
        print(f"✗ Failed to import streamlit: {e}")
        return False

    try:
        import plotly.express as px
        print("✓ Plotly imported")
    except ImportError as e:
        print(f"✗ Failed to import plotly: {e}")
        return False

    try:
        from src.data_loader import load_raw_data, filter_and_clean_data
        print("✓ Data loader module imported")
    except ImportError as e:
        print(f"✗ Failed to import data_loader: {e}")
        return False

    try:
        from src.rfm_engine import calculate_rfm
        print("✓ RFM engine module imported")
    except ImportError as e:
        print(f"✗ Failed to import rfm_engine: {e}")
        return False

    try:
        from src.visuals import (
            plot_funnel_chart,
            plot_weekly_trend,
            plot_hourly_activity,
            plot_rfm_distribution,
        )
        print("✓ Visuals module imported")
    except ImportError as e:
        print(f"✗ Failed to import visuals: {e}")
        return False

    try:
        from src.ai_insights import generate_basic_insights
        print("✓ AI insights module imported")
    except ImportError as e:
        print(f"✗ Failed to import ai_insights: {e}")
        return False

    return True


def test_rfm_engine():
    """Test RFM calculation with sample data."""
    print("\nTesting RFM engine...")
    try:
        from src.rfm_engine import calculate_rfm
        
        # Create sample data
        sample_data = pd.DataFrame(
            {
                "user_id": [1, 1, 2, 2, 2, 3, 4],
                "behavior_type": ["buy", "buy", "buy", "buy", "buy", "buy", "buy"],
                "datetime": pd.to_datetime(
                    [
                        "2017-12-01",
                        "2017-12-02",
                        "2017-11-28",
                        "2017-11-29",
                        "2017-11-30",
                        "2017-11-26",
                        "2017-12-03",
                    ]
                ),
            }
        )

        # Calculate RFM
        rfm_result = calculate_rfm(sample_data)

        if rfm_result.empty:
            print("✗ RFM result is empty")
            return False

        # Check expected columns
        expected_cols = ["Recency", "Frequency", "R_score", "F_score", "Segment"]
        if not all(col in rfm_result.columns for col in expected_cols):
            print(f" Missing expected columns. Found: {rfm_result.columns.tolist()}")
            return False

        print(f"✓ RFM calculation successful. Users: {len(rfm_result)}")
        print(f"  Segments: {rfm_result['Segment'].value_counts().to_dict()}")
        return True

    except Exception as e:
        print(f"✗ RFM engine test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_visuals():
    """Test visualization functions with sample data."""
    print("\nTesting visualization functions...")
    try:
        from src.visuals import (
            plot_funnel_chart,
            plot_weekly_trend,
            plot_hourly_activity,
            plot_rfm_distribution,
        )
        
        # Create sample data
        sample_data = pd.DataFrame(
            {
                "user_id": [1, 2, 3] * 10,
                "item_id": range(30),
                "category_id": [1] * 30,
                "behavior_type": ["pv", "cart", "fav", "buy"] * 7 + ["pv", "cart"],
                "ts": range(1511568000, 1511568030),
                "datetime": pd.date_range("2017-11-25", periods=30, freq="h"),
                "weekday": [0, 1, 2] * 10,
                "hour": list(range(24)) + [0, 1, 2, 3, 4, 5],
                "behavior_cn": ["点击", "加购", "收藏", "购买"] * 7 + ["点击", "加购"],
            }
        )

        # Test funnel chart
        fig = plot_funnel_chart(sample_data)
        if fig is None:
            print(" Funnel chart generation failed")
            return False
        print("✓ Funnel chart generated")

        # Test weekly trend
        fig = plot_weekly_trend(sample_data)
        if fig is None:
            print("✗ Weekly trend generation failed")
            return False
        print("✓ Weekly trend generated")

        # Test hourly activity
        fig = plot_hourly_activity(sample_data)
        if fig is None:
            print("✗ Hourly activity generation failed")
            return False
        print("✓ Hourly activity generated")

        # Test RFM distribution
        rfm_sample = pd.DataFrame(
            {
                "Segment": ["重要价值客户", "潜力客户", "流失客户"] * 2,
                "Count": [10, 20, 15] * 2,
            }
        )
        fig = plot_rfm_distribution(rfm_sample)
        if fig is None:
            print("✗ RFM distribution generation failed")
            return False
        print("✓ RFM distribution generated")

        return True

    except Exception as e:
        print(f"✗ Visualization test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("Taobao User Behavior Analysis - Test Suite")
    print("=" * 60)

    results = []

    # Test imports
    results.append(("Module Imports", test_imports()))

    # Test RFM engine
    results.append(("RFM Engine", test_rfm_engine()))

    # Test visuals
    results.append(("Visualization Functions", test_visuals()))

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{test_name}: {status}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed! The application is ready to run.")
        return 0
    else:
        print(f"\n️  {total - passed} test(s) failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
