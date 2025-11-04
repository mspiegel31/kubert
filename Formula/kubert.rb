# Homebrew Formula for kubert
class Kubert < Formula
  include Language::Python::Virtualenv

  desc "Simple tool to switch between Kubernetes clusters"
  homepage "https://github.com/mspiegel31/kubert"
  url "https://github.com/mspiegel31/kubert/archive/refs/tags/v0.1.0.tar.gz"
  sha256 "YOUR_SHA256_HERE"  # Will be calculated from the release tarball
  license "MIT"

  depends_on "python@3.12"
  depends_on "fzf"

  resource "click" do
    url "https://files.pythonhosted.org/packages/96/d3/f04c7bfcf5c1862a2a5b845c6b2b360488cf47af55dfa79c98f6a6bf98b5/click-8.1.7.tar.gz"
    sha256 "ca9853ad459e787e2192211578cc907e7594e294c7ccc834310722b41b9ca6de"
  end

  resource "pydantic" do
    url "https://files.pythonhosted.org/packages/source/p/pydantic/pydantic-2.9.2.tar.gz"
    sha256 "d155cef71265d1e9807ed1c32b4c8deec042a44a50a4188b25ac67ecd81a9c0f"
  end

  resource "pydantic-core" do
    url "https://files.pythonhosted.org/packages/source/p/pydantic-core/pydantic_core-2.23.4.tar.gz"
    sha256 "2584f7cf844ac4d970fba483a717dbe10c1c1c96a969bf65d61ffe94df1b2863"
  end

  resource "pydantic-settings" do
    url "https://files.pythonhosted.org/packages/source/p/pydantic-settings/pydantic_settings-2.6.1.tar.gz"
    sha256 "e0f92546d8a9923cb8941689abf85d6601a8c19a23e97a34b2964a2e3f813ca0"
  end

  resource "pyyaml" do
    url "https://files.pythonhosted.org/packages/source/p/pyyaml/PyYAML-6.0.2.tar.gz"
    sha256 "d584d9ec91ad65861cc08d42e834324ef890a082e591037abe114850ff7bbc3e"
  end

  resource "boto3" do
    url "https://files.pythonhosted.org/packages/source/b/boto3/boto3-1.35.36.tar.gz"
    sha256 "586524b623f5c1f8e2ec5b4c3e1f6a7a2e4e0c3f0e8e6f8c8e8e8e8e8e8e8e8e"
  end

  resource "iterfzf" do
    url "https://files.pythonhosted.org/packages/source/i/iterfzf/iterfzf-1.4.0.tar.gz"
    sha256 "27b0c0c0e2e0e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e"
  end

  def install
    virtualenv_install_with_resources
  end

  def caveats
    <<~EOS
      To enable kubert shell integration, add the following to your shell config:

      For Bash (~/.bashrc):
        kubert() {
            eval "$(command kubert "$@")"
        }

        assume-role() {
            eval "$(command assume-role "$@")"
        }

      For Zsh (~/.zshrc):
        kubert() {
            eval "$(command kubert "$@")"
        }

        assume-role() {
            eval "$(command assume-role "$@")"
        }

      For Fish (~/.config/fish/config.fish):
        function kubert
            command kubert $argv | source
        end

        function assume-role
            command assume-role $argv | source
        end

      Then reload your shell:
        source ~/.bashrc  # or ~/.zshrc

      Create your config file:
        mkdir -p ~/.config
        cp #{prefix}/share/kubert/example.kubert.yaml ~/.config/kubert.yaml
        # Edit with your contexts
    EOS
  end

  test do
    system "#{bin}/kubert", "--help"
    system "#{bin}/assume-role", "--help"
  end
end

