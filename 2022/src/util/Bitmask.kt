package util

class Bitmask64(private val mask: ULong) {
    fun hasFullOverlapWith(other: Bitmask64): Boolean {
        return this.isContainedIn(other) || other.isContainedIn(this)
    }

    fun hasOverlapWith(other: Bitmask64): Boolean {
        return (mask and other.mask) != 0UL
    }

    fun isContainedIn(other: Bitmask64): Boolean {
        return (mask and other.mask) == mask
    }

    fun isEmpty(): Boolean {
        return mask != 0UL
    }

    override fun toString(): String {
        return (0..63).map { if ((mask and (1UL shl it)) != 0UL) 'X' else '.' }.joinToString("")
    }
}

class LongBitmask(private val masks: Array<Bitmask64>) {
    fun hasFullOverlapWith(other: LongBitmask): Boolean {
        val pairs = masks.zip(other.masks)
        return pairs.all { (a, b) -> a.isContainedIn(b) } ||
                pairs.all { (a, b) -> b.isContainedIn(a) }
    }

    fun hasOverlapWith(other: LongBitmask): Boolean {
        assert(other.masks.size == masks.size)
        return masks.zip(other.masks).any { (a, b) -> a.hasOverlapWith(b) }
    }

    fun isContainedIn(other: LongBitmask): Boolean {
        assert(other.masks.size == masks.size)
        return masks.zip(other.masks).all { (a, b) -> a.isContainedIn(b) }
    }

    override fun toString(): String {
        return masks.joinToString("|")
    }
}

fun Pair<Int,Int>.asRangeLongBitmask(bits: Int): LongBitmask {
    return LongBitmask(( 0 .. (bits-1) / 64).map {
        val base = 64 * it
        val range = first..second
        var mask = 0UL
        for (i in base+63 downTo base) {
            mask = mask shl 1
            if (i in range) mask = mask or 1UL
        }
        Bitmask64(mask)
    }.toTypedArray())
}