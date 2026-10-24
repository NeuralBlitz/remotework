from ruin_recon import RuinSite
from ruin_recon.models import reconstruct_site


def main() -> None:
    site = RuinSite("R1", "Roman Villa", 41.9028, 12.4964, "1st century CE")
    recon = reconstruct_site(site)
    print(f"Site: {site.name}")
    print(f"Completeness: {recon.completeness:.0%}")


if __name__ == "__main__":
    main()
