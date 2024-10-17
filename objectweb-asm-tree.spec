Name:           objectweb-asm-tree
Version:        7.1
Release:        2
Summary:        Tree API of ASM, a very small and fast Java bytecode manipulation framework
License:        BSD
URL:            https://asm.ow2.org/
BuildArch:      noarch
BuildRequires:	jdk-current
BuildRequires:	javapackages-local
BuildRequires:	jmod(org.objectweb.asm)

Source0:        https://repository.ow2.org/nexus/content/repositories/releases/org/ow2/asm/asm-tree/%{version}/asm-tree-%{version}-sources.jar
Source1:        https://repository.ow2.org/nexus/content/repositories/releases/org/ow2/asm/asm-tree/%{version}/asm-tree-%{version}.pom
Patch0:		objectweb-asm-tree-7.1-javadoc-html5.patch

%description
Tree API of ASM, a very small and fast Java bytecode manipulation framework

%package        javadoc
Summary:        API documentation for %{pkg_name}

%description    javadoc
This package provides %{summary}.

%prep
%autosetup -p1 -c asm-tree-%{version}

%build
. %{_sysconfdir}/profile.d/90java.sh
export PATH=$JAVA_HOME/bin:$PATH

cat >module-info.java <<'EOF'
module org.objectweb.asm.tree {
	exports org.objectweb.asm.tree;
	requires org.objectweb.asm;
}
EOF
find . -name "*.java" |xargs javac -p %{_javadir}/modules
javadoc -d docs -sourcepath . org.objectweb.asm.tree -p %{_javadir}/modules
find . -name "*.java" |xargs rm -f
jar cf asm-tree-%{version}.jar META-INF org module-info.class
cp %{S:1} .

%install
mkdir -p %{buildroot}%{_javadir}/modules %{buildroot}%{_mavenpomdir} %{buildroot}%{_javadocdir}
cp asm-tree-%{version}.jar %{buildroot}%{_javadir}
cp *.pom %{buildroot}%{_mavenpomdir}/
%add_maven_depmap asm-tree-%{version}.pom asm-tree-%{version}.jar
cp -a docs %{buildroot}%{_javadocdir}/org.objectweb.asm.tree
mv %{buildroot}%{_javadir}/*.jar %{buildroot}%{_javadir}/modules/
ln -s modules/asm-tree-%{version}.jar %{buildroot}%{_javadir}/
ln -s modules/asm-tree-%{version}.jar %{buildroot}%{_javadir}/asm-tree.jar
ln -s modules/asm-tree-%{version}.jar %{buildroot}%{_javadir}/org.objectweb.asm.tree.jar

%files -f .mfiles
%{_javadir}/*.jar
%{_javadir}/modules/*.jar

%files javadoc
%{_javadocdir}/org.objectweb.asm.tree
