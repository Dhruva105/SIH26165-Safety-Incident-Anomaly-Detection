from safety_anomaly.cli import main

if __name__ == "__main__":
    import sys
    sys.argv = [sys.argv[0], "audit", *sys.argv[1:]]
    main()
