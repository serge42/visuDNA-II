package geneStruct;

import java.util.ArrayList;
import java.util.List;

/**
 * @author Maria Sisto
 *
 * Class that represents a Gene.
 */
class Gene {
	private int ID;
	private String name;
	private List<String> phenotype;

	public Gene(int ID) {
		this.ID = ID;
	}

	public Gene(int ID, String name) {
		this.ID = ID;
		this.name = name;
		this.phenotype = new ArrayList<String>();
	}

	public Gene(int ID, String name, ArrayList<String> phenotype) {
		this.ID = ID;
		this.name = name;
		this.phenotype = phenotype;
	}

	public int getID() {
		return ID;
	}

	public String getName() {
		return name;
	}

	public List<String> getPhenotype() {
		return phenotype;
	}

	public void setPhenotype(ArrayList<String> phenotype) {
		this.phenotype = phenotype;
	}

	public void addPhenotype(List<String> phenotype) {
		this.phenotype.addAll(phenotype);
	}

	public String toString() {
		String ret = ID + " " + name + ": ";
		for (String s: phenotype) {
			ret += s + ", ";
		}
		return ret;
	}

	/**
	 * @Override
	 * Only tests the ID of the gene. Any genes having the same ID are considered equals.
	 */
	public boolean equals(Object o){
		Gene g = (Gene) o;
		return this.ID == g.ID;
	}

	/**
	 * @Override
	 * Only depends on the ID of the gene.
	 */
	public int hashCode() {
		return ID;
	}
}