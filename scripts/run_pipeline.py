from safety_anomaly.cli import main

if __name__ == "__main__":
    import sys
    sys.argv = [sys.argv[0], "run", *sys.argv[1:]]
    main()
