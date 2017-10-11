package geneStruct;

/**
 * @author Maria Sisto
 *
 * Represents an interaction between two genes.
 */
class Interaction {
	private Gene g1;
	private Gene g2;
	private String descr;
	
	public Interaction(Gene g1, Gene g2) {
		this.g1 = g1;
		this.g2 = g2;
		this.descr = "";
	}

	public Interaction(Gene g1, Gene g2, String descr) {
		this.g1 = g1;
		this.g2 = g2;
		this.descr = descr;
	}
	
	public Gene getG1() {
		return g1;
	}
	
	public Gene getG2() {
		return g2;
	}
	
	public String getDescr() {
		return descr;
	}
	
	public void setDescr(String descr) {
		this.descr = descr;
	}
	
	@Override
	public boolean equals(Object o){
		Interaction g = (Interaction) o;
		return this.g1.equals(g.g1) && this.g2.equals(g.g2);
	}

	@Override
	public int hashCode() {
		return g1.hashCode() + g2.hashCode();
	}
	
	public String toString() {
		return g1.getID() + " " + g2.getID();
	}
}