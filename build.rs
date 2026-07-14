fn main() {
    cc::Build::new()
        .file("clib/lib.c")
        .compile("cmod_native");
}
